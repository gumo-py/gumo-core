import dataclasses

from gumo.core.domain.configuration import GoogleCloudLocation
from gumo.core.domain.configuration import GoogleCloudProjectID
from gumo.core.domain.configuration import ApplicationPlatform
from gumo.core.domain.configuration import ServiceAccountCredentialConfig


@dataclasses.dataclass(frozen=True)
class GumoConfiguration:
    google_cloud_project: GoogleCloudProjectID
    google_cloud_location: GoogleCloudLocation
    application_platform: ApplicationPlatform
    service_account_credential_config: ServiceAccountCredentialConfig  # will be deprecated

    @property
    def is_local(self) -> bool:
        return self.application_platform == self.application_platform.Local

    @property
    def is_google_app_engine(self) -> bool:
        return self.application_platform == self.application_platform.GoogleAppEngine
