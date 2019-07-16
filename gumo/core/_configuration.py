from logging import getLogger
from typing import Optional
from injector import singleton

from gumo.core.injector import injector
from gumo.core.infrastructure.configuration import GumoConfiguration

logger = getLogger('gumo.core')


def configure(
        google_cloud_project: Optional[str] = None,
        google_cloud_location: Optional[str] = None,
        service_account_credential_path: Optional[str] = None,
):
    if google_cloud_location is not None:
        logger.warning(f'The argument "google_cloud_location" of gumo.core.configure() is deprecated.')
    if service_account_credential_path is not None:
        logger.warning(f'The argument "service_account_credential_path" of gumo.core.configure() is deprecated.')

    config = GumoConfiguration(
        google_cloud_project=google_cloud_project,
    )
    logger.debug(f'Gumo is configured, config={config}')
    injector.binder.bind(GumoConfiguration, to=config, scope=singleton)

    return config
