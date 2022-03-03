from os.path import join

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import exceptions as jwt_ext_exceptions
from flask_restx import Api as _Api
from flask_restx import Namespace
from jwt import exceptions as jwt_exceptions
from werkzeug.middleware.proxy_fix import ProxyFix

from .resource import make_resource


class Api(_Api):
    def error_router(self, original_handler, e):
        """ Override original error_router to only custom errors and parsing error (from webargs)"""
        # adapted from https://github.com/vimalloc/flask-jwt-extended/issues/141#issuecomment-569524817
        error_type = type(e).__name__.split(".")[-1] # extract the error class name as a string
        if self._has_fr_route() and error_type not in dir(jwt_exceptions) + dir(jwt_ext_exceptions):
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler

        return original_handler(e)

def make_app(functions, name, prefix='/', max_content_length=None, origins=None, secret_key=None):
    if secret_key:
        authorizations = {
            'bearer_token': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        }
    else:
        authorizations = None

    api = Api(title=name, authorizations=authorizations)
    app = Flask(__name__)

    if secret_key is not None:
        app.config['JWT_SECRET_KEY'] = secret_key
        app.config['JWT_TOKEN_LOCATION'] = ['headers']
        app.config['PROPAGATE_EXCEPTIONS'] = False
        jwt = JWTManager(app)
        @jwt.unauthorized_loader
        def unathenticated(msg):
            return {'message': msg}, 401

    if origins is not None:
        CORS(app, resources={r'{}'.format(join('/', prefix, '*')): {"origins": origins}})
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    if max_content_length is not None:
        app.config['MAX_CONTENT_LENGTH'] = max_content_length
    app.wsgi_app = ProxyFix(app.wsgi_app,
                            x_for=1, x_proto=1,
                            x_host=1, x_port=1,
                            x_prefix=1)

    @api.errorhandler(Exception)
    def _default_error(error):
        return {'message': repr(error)}, 500

    ns = Namespace(prefix, description='Tranquilized API')

    for f in functions:
        if f._requires_authentication is None:
            requires_authentication = False if secret_key is None else True
        elif f._requires_authentication and secret_key is None:
            raise RuntimeError('The function "{name}()" has been tranquilized with requires_authentication=True '
                               'but the --secret-key <secret-key> command-line argument was not supplied when '
                               'running tranquilizer.'.format(name=f.__name__))
        else:
            requires_authentication = f._requires_authentication
        resource = make_resource(f, ns, requires_authentication=requires_authentication)
        ns.add_resource(resource, '/{}'.format(f._spec['name']))
        api.add_namespace(ns)

    api.init_app(app)

    return app

