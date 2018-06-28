from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api, Namespace
from argparse import ArgumentParser

from .resource import make_resource

def cli():
    # arg parser for the standard anaconda-project options
    parser = ArgumentParser(prog="tranquil",
                            description="Serve API from script file")
    parser.add_argument('filename', help='File with tranquilized functions')
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
    api = Api(title='tranquil api')
    app = Flask(__name__)
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.wsgi_app = ProxyFix(app.wsgi_app)

    ns = Namespace('/', 'Tranquil API')

    for f in functions:
        resource = make_resource(f, ns)
        ns.add_resource(resource, '/{}'.format(f._spec['name']))
        api.add_namespace(ns)

    api.init_app(app)

    return app

