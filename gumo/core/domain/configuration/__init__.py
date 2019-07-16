import dataclasses
import enum


@dataclasses.dataclass(frozen=True)
class GoogleCloudProjectID:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValueError(f'project_id must be a string, expect: {type(self.value)}')


class ApplicationPlatform(enum.Enum):
    Local = 'local'
    GoogleAppEngine = 'google-app-engine'
