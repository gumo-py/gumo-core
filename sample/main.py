import flask
import logging
import sys
import os

from gumo.core import configure as core_configure

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'gumo-core-test'

core_configure()


app = flask.Flask(__name__)


@app.route('/')
def hello():
    return f'Hello, world. (gumo-core)'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
