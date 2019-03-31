from gumo.core.injector import injector
from gumo.core.infrastructure.credential import CredentialManager
from gumo.core.domain.configuration import ServiceAccountCredentialConfig


def test_credential_manager():
    o = injector.get(CredentialManager)  # type: CredentialManager
    assert isinstance(o, CredentialManager)
    assert isinstance(o._credential_config, ServiceAccountCredentialConfig)
