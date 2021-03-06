import os

from gumo.core import configure as gumo_configure
from gumo.core.injector import injector
from gumo.core.infrastructure.credential import GoogleOAuthCredentialManager

from google.oauth2.service_account import Credentials
from google.oauth2.service_account import IDTokenCredentials
from google.auth.transport.requests import Request


gumo_configure()


class TestCredentialManager:
    def setup_method(self, method):
        self.env_vars = {}
        for k, v in os.environ.items():
            self.env_vars[k] = v

    def teardown_method(self, method):
        for k in os.environ.keys():
            if k not in self.env_vars:
                del os.environ[k]

        for k, v in self.env_vars.items():
            os.environ[k] = v

    def prepare_credential(self):
        if 'GOOGLE_APPLICATION_CREDENTIALS_FOR_TEST' in os.environ:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ['GOOGLE_APPLICATION_CREDENTIALS_FOR_TEST']

    def test_credential_manager(self):
        self.prepare_credential()
        o = injector.get(GoogleOAuthCredentialManager)  # type: GoogleOAuthCredentialManager
        assert isinstance(o, GoogleOAuthCredentialManager)

    def test_build_credential_with_google_application_credentials(self):
        self.prepare_credential()
        assert 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ
        assert os.path.exists(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

        manager = injector.get(GoogleOAuthCredentialManager)  # type: GoogleOAuthCredentialManager
        cred = manager.build_credentials()

        assert isinstance(cred, Credentials)
        assert cred.signer_email.index('@') > 0
        assert cred.signer_email.index('gserviceaccount.com') > 0

    def test_build_id_token_credential_with_google_application_credentials(self):
        self.prepare_credential()
        assert 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ
        assert os.path.exists(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

        target_audience = os.environ.get(
            'TEST_TARGET_AUDIENCE',
            '204100934405-b9gjp2hnbtq12r9s4i460mmrsjl1jvg4.apps.googleusercontent.com'
        )
        manager = injector.get(GoogleOAuthCredentialManager)  # type: GoogleOAuthCredentialManager
        id_token_credential, request = manager.build_id_token_credentials(
            target_audience=target_audience
        )

        assert isinstance(id_token_credential, IDTokenCredentials)
        assert isinstance(request, Request)

        assert id_token_credential.signer_email.index('@') > 0
        assert id_token_credential.signer_email.index('gserviceaccount.com') > 0
        assert id_token_credential.service_account_email.index('gserviceaccount.com') > 0
