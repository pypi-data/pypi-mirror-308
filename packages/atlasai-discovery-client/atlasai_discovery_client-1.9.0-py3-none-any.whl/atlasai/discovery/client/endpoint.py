# Copyright 2024 AtlasAI PBC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hmac
from importlib.metadata import version
import logging
import os
from urllib.parse import urlparse
import warnings

import arrow
import requests
from requests.adapters import HTTPAdapter, Retry
from sgqlc.endpoint.requests import RequestsEndpoint

from . import constants
from .retry import retry

logger = logging.getLogger(__name__)

CONNECT_TIMEOUT = 10 # in seconds
READ_TIMEOUT = 1800 # in seconds

DEFAULT_READ_RETRIES_STATUS_LIST = [429, 500, 502, 503, 504]
DEFAULT_WRITE_RETRIES_STATUS_LIST = [429, 502, 503]

X_PRODUCT_NAME = 'Discovery'

def get_url():
    url = os.getenv(constants.DISCOVERY_GRAPHQL_URL)
    if not url:
        raise RuntimeError(f'Missing Discovery GraphQL URL. Provide the Environment variable: {constants.DISCOVERY_GRAPHQL_URL}')
    return url


def _create_requests_session():
    s = requests.Session()
    headers = {}
    include_client_headers(headers)
    s.headers.update(headers)

    return s


def get_requests_session():
    enable_read_retries = os.getenv(constants.ENABLE_DISCOVERY_READ_RETRIES)
    enable_write_retries = os.getenv(constants.ENABLE_DISCOVERY_WRITE_RETRIES)
    if not enable_read_retries and not enable_write_retries:
        return _create_requests_session()

    status_list = (
        DEFAULT_READ_RETRIES_STATUS_LIST
        if enable_read_retries
        else DEFAULT_WRITE_RETRIES_STATUS_LIST
    )

    sess = _create_requests_session()
    if os.getenv(constants.DISABLE_SSL_VERIFICATION):
        sess.verify = False
    retries = Retry(
        total=10,
        backoff_factor=0.2,
        allowed_methods=None,
        status_forcelist=status_list,
    )
    sess.mount('https://', HTTPAdapter(max_retries=retries))

    return sess


def include_client_headers(headers):
    client_version = version('atlasai-discovery-client')
    headers['User-Agent'] = f'atlasai/discovery-client-{client_version}'
    headers['X-Discovery-Client-Version'] = client_version


def get_endpoint(url, headers=None, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)):
    url = url or get_url()

    headers = headers or {}
    include_client_headers(headers)

    return RequestsEndpoint(
        url,
        base_headers=headers, # not necessary but just in case
        timeout=timeout,
        session=get_requests_session(),
    )


@retry(attempts=10, backoff_factor=0.3)
def query(query, variables=None, url=None, headers=None, x_product_name=None):
    variables = variables or {}
    endpoint = get_endpoint(url, headers)
    include_authorization(
        endpoint.url,
        endpoint.base_headers,
        x_product_name=x_product_name
    )
    return endpoint(query, variables)

def get_secret_data(secret_id):
    try:
        from google.api_core.retry import Retry
        from google.cloud import secretmanager
    except ImportError:
        logger.warning('Client library not found: google-cloud-secret-manager')
        return None

    try:
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(
            request={
                'name': secret_id,
            },
            retry=Retry(),
        )
    except Exception as e:
        logger.error(f'Error getting data from Secret Manager: {secret_id} {e}')
        raise
    else:
        return response.payload.data.decode('utf-8')

def load_credentials(access_key=None, secret_key=None):
    access_key = access_key or os.getenv('DISCOVERY_ACCESS_KEY')
    secret_key = secret_key or os.getenv('DISCOVERY_SECRET_KEY')
    api_secret = os.getenv('DISCOVERY_API_SECRET')

    if not secret_key and api_secret:
        secret_key = get_secret_data(api_secret)
        if secret_key is not None:
            os.environ['DISCOVERY_SECRET_KEY'] = secret_key

    return access_key, secret_key


def include_authorization(
    url,
    headers,
    bearer_token=None,
    access_key=None,
    secret_key=None,
    x_product_name=None,
):
    x_product_name = x_product_name or X_PRODUCT_NAME
    bearer_token = bearer_token or os.getenv('DISCOVERY_BEARER_TOKEN')
    access_key, secret_key = load_credentials(
        access_key=access_key,
        secret_key=secret_key,
    )

    if bearer_token:
        headers['Authorization'] = f'Bearer {bearer_token}'
        return

    if not access_key and not secret_key:
        warnings.warn('No API Keys provided to access Discovery GraphQL. Provide the following: DISCOVERY_BEARER_TOKEN or the pair DISCOVERY_ACCESS_KEY and DISCOVERY_SECRET_KEY')
        return
    elif any([
        access_key is None,
        secret_key is None,
    ]):
        raise ValueError('DISCOVERY_ACCESS_KEY and DISCOVERY_SECRET_KEY must be provided together')

    product, version = 'discovery', '1'
    headers.update({
        'Host': urlparse(url).netloc,
        f'X-{x_product_name}-Date': arrow.utcnow().isoformat(),
        f'X-{x_product_name}-Credential': '/'.join([product, version, access_key]),
        f'X-{x_product_name}-SignedHeaders': 'x-discovery-date;x-discovery-credential;host',
    })

    sign_request(headers, secret_key, x_product_name=x_product_name)


def sign_request(headers, secret_key, x_product_name=None):
    x_product_name = x_product_name or X_PRODUCT_NAME
    product, version, access_key = headers[f'X-{x_product_name}-Credential'].split('/')
    key = f'{product}{version}{secret_key}'.encode('utf-8')
    for msg in (
        headers[f'X-{x_product_name}-Date'],
        f'{product}_{version}_request',
    ):
        obj = hmac.new(key, msg.encode('utf-8'), 'sha256')
        key = obj.digest()

    msg = '\n'.join([
        headers[f'X-{x_product_name}-Date'],
        headers[f'X-{x_product_name}-Credential'],
        headers['Host']
    ])
    headers[f'X-{x_product_name}-Signature'] = hmac.new(key, msg.encode('utf-8'), 'sha256').hexdigest()
