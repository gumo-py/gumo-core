import pytest

from gumo.core._configuration import ConfigurationFactory
from gumo.core import GumoConfiguration
from gumo.core import GoogleCloudLocation
from gumo.core import GoogleCloudProjectID
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
    )


def test_configuration_factory_build_failed():
    with pytest.raises(ValueError):
        ConfigurationFactory.build(
            google_cloud_project='test-project',
            google_cloud_location='unknown-location'
        )
