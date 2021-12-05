from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Api, Namespace
from flask_cors import CORS
from os.path import join

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from .resource import make_resource

def make_app(functions, name, prefix='/', max_content_length=None, origins=None, jwt_secret_key=None):
    if jwt_secret_key:
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

    if jwt_secret_key is not None:
        app.config['JWT_SECRET_KEY'] = jwt_secret_key
        jwt = JWTManager(app)

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
        protected = False if jwt_secret_key is None else True
        resource = make_resource(f, ns, protected=protected)
        ns.add_resource(resource, '/{}'.format(f._spec['name']))
        api.add_namespace(ns)

    api.init_app(app)

    if jwt_secret_key:
        with app.app_context():
            token = create_access_token(identity=f'{name} API user')
        print(token)


    return app

