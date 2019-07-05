import flask
import logging
import sys
import os
import datetime
import hashlib

from gumo.core import configure as core_configure
from gumo.core import get_google_oauth_credentials
from gumo.core import get_google_id_token_credentials

TARGET_AUDIENCE = '204100934405-b9gjp2hnbtq12r9s4i460mmrsjl1jvg4.apps.googleusercontent.com'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'gumo-core-test'

core_configure()


app = flask.Flask(__name__)


@app.route('/')
def hello():
    return f'Hello, world. (gumo-core)'


@app.route('/credential')
def credential():
    cred = get_google_oauth_credentials()

    result = [str(cred)]
    result.append('')
    result.append(f'service_account_email = {cred.service_account_email}')
    result.append(f'valid = {cred.valid}')
    result.append(f'token (sha256) = {hashlib.sha256(cred.token.encode("utf-8")).hexdigest() if cred.token else None}')
    result.append(f'expired = {cred.expired}')
    result.append(f'expiry = {cred.expiry}')
    result.append(f'now = {datetime.datetime.utcnow()}')

    return flask.Response(
        '\n'.join(result),
        content_type='text/plain'
    )


@app.route('/id_token_credential')
def id_token_credential():
    cred, request = get_google_id_token_credentials(
        target_audience=TARGET_AUDIENCE
    )

    result = [str(cred)]
    result.append('')
    result.append(f'signer_email = {cred.signer_email}')
    result.append(f'service_account_email = {cred.service_account_email}')
    result.append(f'valid = {cred.valid}')
    result.append(f'token (sha256) = {hashlib.sha256(cred.token.encode("utf-8")).hexdigest() if cred.token else None}')
    result.append(f'expired = {cred.expired}')
    result.append(f'expiry = {cred.expiry}')
    result.append(f'now = {datetime.datetime.utcnow()}')

    return flask.Response(
        '\n'.join(result),
        content_type='text/plain'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
