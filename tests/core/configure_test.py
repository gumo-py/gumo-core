import pytest

from gumo.core._configuration import ConfigurationFactory
from gumo.core import GumoConfiguration
from gumo.core.domain.configuration import GoogleCloudLocation
from gumo.core.domain.configuration import GoogleCloudProjectID
from gumo.core.domain.configuration import ServiceAccountCredentialConfig
from gumo.core.domain.configuration import ApplicationPlatform


def test_configuration_factory_build():
    o = ConfigurationFactory.build(
        google_cloud_project='test-project',
        google_cloud_location='asia-northeast1'
    )

    assert o == GumoConfiguration(
        google_cloud_project=GoogleCloudProjectID('test-project'),
        google_cloud_location=GoogleCloudLocation('asia-northeast1'),
        application_platform=ApplicationPlatform.Local,
        service_account_credential_config=ServiceAccountCredentialConfig(enabled=False),
    )


def test_configuration_factory_build_failed():
    with pytest.raises(ValueError):
        ConfigurationFactory.build(
            google_cloud_project='test-project',
            google_cloud_location='unknown-location'
        )


def test_configuration_with_credential_config():
    o = ConfigurationFactory.build(
        google_cloud_project='test-project',
        google_cloud_location='asia-northeast1',
        service_account_credential_path='gs://sample-bucket/credential.json',
    )

    assert o == GumoConfiguration(
        google_cloud_project=GoogleCloudProjectID('test-project'),
        google_cloud_location=GoogleCloudLocation('asia-northeast1'),
        application_platform=ApplicationPlatform.Local,
        service_account_credential_config=ServiceAccountCredentialConfig(
            enabled=True,
            bucket_name='sample-bucket',
            blob_path='credential.json'
        ),
    )
