from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Api, Namespace

from .resource import make_resource

def make_app(functions, name, prefix='/', max_content_length=None):
    api = Api(title=name)
    app = Flask(__name__)
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    if max_content_length is not None:
        app.config['MAX_CONTENT_LENGTH'] = max_content_length
    app.wsgi_app = ProxyFix(app.wsgi_app,
                            # num_proxies=None,
                            x_for=1, x_proto=1,
                            x_host=1, x_port=1,
                            x_prefix=1)

    @api.errorhandler
    def _default_error(error):
        return {'message': repr(error)}, 500

    ns = Namespace(prefix, description='Tranquilized API')

    for f in functions:
        resource = make_resource(f, ns)
        ns.add_resource(resource, '/{}'.format(f._spec['name']))
        api.add_namespace(ns)

    api.init_app(app)

    return app

