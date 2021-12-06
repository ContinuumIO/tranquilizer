from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Api, Namespace
from flask_cors import CORS
from os.path import join

from flask_jwt_extended import JWTManager

from .resource import make_resource

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
        app.config['PROPAGATE_EXCEPTIONS'] = True
        jwt = JWTManager(app)
        @jwt.unauthorized_loader
        def unathenticated(msg):
            return jsonify('Authentication is required'), 401

    if origins is not None:
        CORS(app, resources={r'{}'.format(join('/', prefix, '*')): {"origins": origins}})
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
        if f._protected is None:
            protected = False if secret_key is None else True
        elif f._protected and secret_key is None:
            raise RuntimeError(f'The function "{f.__name__}()" has been tranquilized with protected=True but the '
                               f'--secret-key <secret-key> command-line argument was not supplied when running '
                               f'tranquilizer.')
        else:
            protected = f._protected
        resource = make_resource(f, ns, protected=protected)
        ns.add_resource(resource, '/{}'.format(f._spec['name']))
        api.add_namespace(ns)

    api.init_app(app)

    return app

