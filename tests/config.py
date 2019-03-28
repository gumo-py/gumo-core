import os


if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/credential.json'
