from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api

from namespace import make_api_namespace
from parser import prepare
from cli import cli

# The global application and api
# all decorated functions are endpoints
API = Api(title='comatose api')
APP = Flask(__name__)
APP.config['PREFERRED_URL_SCHEME'] = 'https'
APP.wsgi_app = ProxyFix(APP.wsgi_app)


def publish(methods=None):
    """Decorator function that gets a function wraps it in order to
    append a function spec (see prepare function) and autocast args/kws
    to match types.
    """
    if not methods:
        methods = ["GET"]

    def expose_wrapper(f):
        f._spec = prepare(f)
        f._methods = methods

        ns = make_api_namespace(f)
        API.add_namespace(ns)

    return expose_wrapper

def main():
    args = cli().parse_args()

    ## read and execute filename

    API.init_app(APP)
    APP.run(host=args.anaconda_project_address, port=args.anaconda_project_port)

if __name__ == '__main__':
    from arg_types import ParsedDateTime

    @publish(['GET'])
    def func1(a: str, b: ParsedDateTime, c: int = 10):
        return {'a':a, 'b':b.strftime('%c'), 'c':c}

    @publish(['GET'])
    def func2(d, e):
        return {'d':d, 'e':e}

    API.init_app(APP)
    APP.run()
