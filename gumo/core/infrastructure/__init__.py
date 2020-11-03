import os
from typing import Dict

import yaml

from logging import getLogger
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader

logger = getLogger(__name__)


class MockAppEngineEnvironment:
    @classmethod
    def load_app_yaml(cls, app_yaml_path):
        with open(app_yaml_path, 'r+') as f:
            app_yaml = yaml.load(f, Loader=Loader)

        if 'env_variables' not in app_yaml:
            logger.debug('"env_variables" doest not exists in app.yaml')
        else:
            logger.debug('"env_variables" exists in app.yaml:')
            cls._set_env_variables(env_variables=app_yaml["env_variables"])

    @classmethod
    def _set_env_variables(cls, env_variables: Dict[str, str]) -> None:
        for key, value in env_variables.items():
            if os.environ.get(key):
                logger.debug(f' * os.environ["{key}"] ... skipped (current value= {os.environ.get(key)}')
            else:
                os.environ[key] = str(value)
                logger.debug(f' * os.environ["{key}"] = "{str(value)}"')
