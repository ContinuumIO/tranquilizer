from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api
from argparse import ArgumentParser, FileType

from namespace import make_api_namespace

def cli():
    # arg parser for the standard anaconda-project options
    parser = ArgumentParser(prog="api",
                            description="Serve API from script file")
    parser.add_argument('filename', help='File with published functions', type=FileType('r'))
    parser.add_argument('--anaconda-project-host', action='append', default=[],
                        help='Hostname to allow in requests')
    parser.add_argument('--anaconda-project-port', action='store', default=8086, type=int,
                        help='Port to listen on')
    parser.add_argument('--anaconda-project-iframe-hosts',
                        action='append',
                        help='Space-separated hosts which can embed us in an iframe per our Content-Security-Policy')
    parser.add_argument('--anaconda-project-no-browser', action='store_true',
                        default=False,
                        help='Disable opening in a browser')
    parser.add_argument('--anaconda-project-use-xheaders',
                        action='store_true',
                        default=False,
                        help='Trust X-headers from reverse proxy')
    parser.add_argument('--anaconda-project-url-prefix', action='store', default='',
                        help='Prefix in front of urls')
    parser.add_argument('--anaconda-project-address',
                        action='store',
                        default='0.0.0.0',
                        help='IP address the application should listen on.')

    return parser


def make_app(functions):
    api = Api(title='comatose api')
    app = Flask(__name__)
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.wsgi_app = ProxyFix(app.wsgi_app)

    for f in functions:
        ns = make_api_namespace(f)
        api.add_namespace(ns)

    api.init_app(app)

    return app


if __name__ == '__main__':
    from arg_types import ParsedDateTime
    from publisher import publish

    @publish(['get'])
    def func1(a: str, b: ParsedDateTime, c: int = 10):
        return {'a':a, 'b':b.strftime('%c'), 'c':c}

    @publish(['get'])
    def func2(d, e):
        return {'d':d, 'e':e}

    app = make_app([func1, func2])
    app.run()
