from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api, Namespace
from argparse import ArgumentParser

from .resource import make_resource
from .__init__ import __version__

def cli():
    parser = ArgumentParser(prog="tranquilizer",
                            description="Put your functions to REST")
    parser.add_argument('filename', help='Script file with tranquilized functions')
    parser.add_argument('--name', help='Name of the REST API to use in Swagger')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Run API with debug output.')
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

    # arg parser for the standard anaconda-project options
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


def make_app(functions, name, prefix='/'):
    api = Api(title=name)
    app = Flask(__name__)
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @api.errorhandler
    def _default_error(error):
        return {'message':repr(error)}, 500

    ns = Namespace(prefix, description='Tranquilized API')

    for f in functions:
        resource = make_resource(f, ns)
        ns.add_resource(resource, '/{}'.format(f._spec['name']))
        api.add_namespace(ns)

    api.init_app(app)

    return app

