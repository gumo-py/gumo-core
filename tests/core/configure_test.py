import pytest
import os

from gumo.core.domain.configuration import ApplicationPlatform
from gumo.core.infrastructure.configuration import GumoConfiguration


class TestGumoConfiguration:
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

    def test_build_success_in_local(self):
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None
        assert 'GAE_DEPLOYMENT_ID' not in os.environ
        assert 'GAE_INSTANCE' not in os.environ

        o = GumoConfiguration()

        assert o.google_cloud_project.value == os.environ['GOOGLE_CLOUD_PROJECT']
        assert o.application_platform == ApplicationPlatform.Local
        assert o.is_local

    def test_build_success_in_app_engine_platform(self):
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None
        os.environ['GAE_DEPLOYMENT_ID'] = 'deployment-id'
        os.environ['GAE_INSTANCE'] = 'app-engine-instance-id'

        o = GumoConfiguration()

        assert o.google_cloud_project.value == os.environ['GOOGLE_CLOUD_PROJECT']
        assert o.application_platform == ApplicationPlatform.GoogleAppEngine
        assert o.is_google_app_engine

    def test_build_failure_mismatch_with_args_and_env_vars(self):
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None

        with pytest.raises(RuntimeError, match='Env-var "GOOGLE_CLOUD_PROJECT" is invalid or undefined.'):
            GumoConfiguration(
                google_cloud_project='example-google-cloud-project-id'
            )
