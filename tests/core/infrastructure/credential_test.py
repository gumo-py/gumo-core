from gumo.core.injector import injector
from gumo.core.infrastructure.credential import CredentialManager
from gumo.core.domain.configuration import ServiceAccountCredentialConfig
from gumo.core.exceptions import ServiceAccountConfigurationError
from google.oauth2.service_account import Credentials


def test_credential_manager():
    o = injector.get(CredentialManager)  # type: CredentialManager
    assert isinstance(o, CredentialManager)
    assert isinstance(o._credential_config, ServiceAccountCredentialConfig)


def test_credential():
    try:
        cred = CredentialManager.get_credential()
    except ServiceAccountConfigurationError as e:
        print(f'ServiceAccountConfigurationError: {e}')
        print('Test skipped.')
        return

    assert isinstance(cred, Credentials)
    assert cred.signer_email.index('@') > 0
    assert cred.signer_email.index('gserviceaccount.com') > 0
