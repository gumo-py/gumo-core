import os

from gumo.core import configure as core_configure

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/credential.json'


core_configure(
    google_cloud_project='gumo-sample',
    google_cloud_location='asia-northeast1',
)
