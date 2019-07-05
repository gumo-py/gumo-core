import os
import dataclasses
import threading

from typing import Optional
from typing import Union
from typing import ClassVar

from gumo.core.domain.configuration import GoogleCloudProjectID
from gumo.core.domain.configuration import ApplicationPlatform


@dataclasses.dataclass(frozen=False)
class GumoConfiguration:
    google_cloud_project: Union[GoogleCloudProjectID, str, None] = None
    application_platform: Optional[ApplicationPlatform] = None

    _ENV_KEY_GOOGLE_CLOUD_PROJECT: ClassVar = 'GOOGLE_CLOUD_PROJECT'
    _lock: ClassVar = threading.Lock()

    def __post_init__(self):
        with self._lock:
            self._set_google_cloud_project()
            self._set_application_platform()

    def _set_google_cloud_project(self):
        if isinstance(self.google_cloud_project, str):
            self.google_cloud_project = GoogleCloudProjectID(self.google_cloud_project)
        if isinstance(self.google_cloud_project, GoogleCloudProjectID):
            if self.google_cloud_project.value != os.environ.get(self._ENV_KEY_GOOGLE_CLOUD_PROJECT):
                raise RuntimeError(f'Env-var "{self._ENV_KEY_GOOGLE_CLOUD_PROJECT}" is invalid or undefined.'
                                   f'Please set value "{self.google_cloud_project.value}" to env-vars.')

        if self.google_cloud_project is None:
            if self._ENV_KEY_GOOGLE_CLOUD_PROJECT in os.environ:
                self.google_cloud_project = GoogleCloudProjectID(os.environ[self._ENV_KEY_GOOGLE_CLOUD_PROJECT])
            else:
                raise RuntimeError(f'Env-var "{self._ENV_KEY_GOOGLE_CLOUD_PROJECT}" is undefined, please set it.')

    def _set_application_platform(self):
        is_google_platform = 'GAE_DEPLOYMENT_ID' in os.environ and 'GAE_INSTANCE' in os.environ
        if is_google_platform:
            self.application_platform = ApplicationPlatform.GoogleAppEngine
        else:
            self.application_platform = ApplicationPlatform.Local

    @property
    def is_local(self) -> bool:
        return self.application_platform == self.application_platform.Local

    @property
    def is_google_app_engine(self) -> bool:
        return self.application_platform == self.application_platform.GoogleAppEngine
