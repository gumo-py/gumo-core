import os
import json

from logging import getLogger
from injector import singleton

from typing import Optional
from typing import Union
from typing import Tuple

import google.auth.transport.requests
from google.oauth2 import service_account
from google.auth import compute_engine
from injector import inject

from gumo.core.exceptions import ServiceAccountConfigurationError
from gumo.core.injector import injector
from gumo.core.infrastructure.configuration import GumoConfiguration

logger = getLogger(__name__)

DEFAULT_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'

Credentials = Union[service_account.Credentials, compute_engine.Credentials]
IDTokenCredentials = Union[service_account.IDTokenCredentials, compute_engine.IDTokenCredentials]
Request = google.auth.transport.Request


class _GoogleCredentialManagerForServiceAccountCredential:
    def __init__(
            self,
            credential_file_path: str,
    ):
        self._credential_file_path = credential_file_path

        self._credentials: Optional[Credentials] = None
        self._id_token_credentials: Optional[IDTokenCredentials] = None

    def build_credentials(self) -> Credentials:
        try:
            if not self._credentials:
                logger.debug('Loading service_account.Credentials from local file.')
                self._credentials = service_account.Credentials.from_service_account_info(
                    info=self._get_content_from_local_file()
                )

            return self._credentials
        except ServiceAccountConfigurationError:
            raise
        except RuntimeError as e:
            raise ServiceAccountConfigurationError(e)

    def _build_request(self) -> Request:
        return google.auth.transport.requests.Request()

    def build_id_token_credentials(
            self,
            target_audience: str,
            token_uri: Optional[str] = None,
    ) -> Tuple[IDTokenCredentials, Request]:
        request = self._build_request()

        try:
            if not self._id_token_credentials or not self._id_token_credentials.valid:
                logger.debug('Build service_account.IDTokenCredentials and token refresh.')

                _credential = self.build_credentials()
                self._id_token_credentials = service_account.IDTokenCredentials(
                    signer=_credential.signer,
                    service_account_email=_credential.service_account_email,
                    token_uri=token_uri if token_uri else DEFAULT_TOKEN_URI,
                    target_audience=target_audience,
                )
                self._id_token_credentials.refresh(request=request)

            return (self._id_token_credentials, request)
        except ServiceAccountConfigurationError:
            raise
        except RuntimeError as e:
            raise ServiceAccountConfigurationError(e)

    def _get_content_from_local_file(self):
        if not os.path.exists(self._credential_file_path):
            raise ServiceAccountConfigurationError(
                f'GOOGLE_APPLICATION_CREDENTIALS={self._credential_file_path} is not found.'
            )

        with open(self._credential_file_path, 'r') as f:
            content = f.read()

        return json.loads(content)


class _GoogleCredentialManagerForComputeEngine:
    def __init__(self):
        self._credentials: Optional[Credentials] = None
        self._id_token_credentials: Optional[IDTokenCredentials] = None

    def _build_request(self) -> Request:
        return google.auth.transport.requests.Request()

    def build_credentials(self) -> Credentials:
        try:
            if not self._credentials or not self._credentials.valid:
                logger.debug('Fetch compute_engine.Credentials and token refresh.')

                self._credentials = compute_engine.Credentials()
                self._credentials.refresh(request=self._build_request())

            return self._credentials
        except ServiceAccountConfigurationError:
            raise
        except RuntimeError as e:
            raise ServiceAccountConfigurationError(e)

    def build_id_token_credentials(
            self,
            target_audience: str,
            token_uri: Optional[str] = None,
    ) -> Tuple[IDTokenCredentials, Request]:
        request = self._build_request()

        try:
            if not self._id_token_credentials or not self._id_token_credentials.valid:
                logger.debug('Fetch compute_engine.IDTokenCredentials and token refresh.')

                self._id_token_credentials = compute_engine.IDTokenCredentials(
                    request=request,
                    target_audience=target_audience,
                    token_uri=token_uri if token_uri else DEFAULT_TOKEN_URI,
                )
                self._id_token_credentials.refresh(request=request)

        except ServiceAccountConfigurationError:
            raise
        except RuntimeError as e:
            raise ServiceAccountConfigurationError(e)

        return (self._id_token_credentials, request)


class GoogleOAuthCredentialManager:
    _ENV_KEY_GOOGLE_APPLICATION_CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS'

    @inject
    def __init__(
            self,
            gumo_configuration: GumoConfiguration,
    ):
        self._gumo_configuration = gumo_configuration
        if self._gumo_configuration.is_google_app_engine:
            self._manager = _GoogleCredentialManagerForComputeEngine()
        elif self._gumo_configuration.is_local:
            self._manager = _GoogleCredentialManagerForServiceAccountCredential(
                credential_file_path=os.environ.get(self._ENV_KEY_GOOGLE_APPLICATION_CREDENTIALS)
            )
        else:
            raise RuntimeError(f'Unknown Platform configuration of GumoConfiguration.')

    def build_credentials(self) -> Credentials:
        return self._manager.build_credentials()

    def _build_request(self) -> Request:
        return google.auth.transport.requests.Request()

    def build_id_token_credentials(
            self,
            target_audience: str,
            with_refresh: bool = True,
            token_uri: Optional[str] = None,
    ) -> Tuple[IDTokenCredentials, Request]:
        _ = with_refresh  # deprecated arguments.

        return self._manager.build_id_token_credentials(
            target_audience=target_audience,
            token_uri=token_uri,
        )


def get_google_oauth_credentials() -> Credentials:
    return injector.get(GoogleOAuthCredentialManager, scope=singleton).build_credentials()


def get_google_id_token_credentials(
        target_audience: str,
        with_refresh: bool = True,
        token_uri: Optional[str] = None,
) -> Tuple[IDTokenCredentials, Request]:
    return injector.get(GoogleOAuthCredentialManager, scope=singleton).build_id_token_credentials(
        target_audience=target_audience,
        with_refresh=with_refresh,
        token_uri=token_uri,
    )
