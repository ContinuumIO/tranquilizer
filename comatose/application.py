'''this is my api'''
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api


def make_app():
    api = Api(title='comatose api')
    api.add_namespace(ns)

    app = Flask(__name__)
    api.init_app(app)

    app.config['PREFERRED_URL_SCHEME'] = 'https'

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app



if __name__ == '__main__':
    from wrapper import publish
    from arg_types import ParsedDateTime

    @publish(['GET'])
    def func(a: str, b: ParsedDateTime, c: int = 10):
        return {'a':a, 'b':b.strftime('%c'), 'c':c}

    make_app(func).run()
