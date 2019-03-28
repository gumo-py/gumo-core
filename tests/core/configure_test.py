import pytest
import os

from gumo.core._configuration import ConfigurationFactory
from gumo.core.domain import GumoConfiguration
from gumo.core.domain import GoogleCloudLocation
from gumo.core.domain import GoogleCloudProjectID
from gumo.core.domain import ApplicationPlatform

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/credential.json'


def test_configuration_factory_build():
    o = ConfigurationFactory.build(
        google_cloud_project='test-project',
        google_cloud_location='asia-northeast1'
    )

    assert o == GumoConfiguration(
        google_cloud_project=GoogleCloudProjectID('test-project'),
        google_cloud_location=GoogleCloudLocation('asia-northeast1'),
        application_platform=ApplicationPlatform.Local,
    )


def test_configuration_factory_build_failed():
    with pytest.raises(ValueError):
        ConfigurationFactory.build(
            google_cloud_project='test-project',
            google_cloud_location='unknown-location'
        )
