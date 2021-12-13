import pytest
from tranquilizer.application import make_app
from tranquilizer.handler import ScriptHandler
from werkzeug.middleware.proxy_fix import ProxyFix
from os.path import dirname, join

@pytest.fixture
def tranquilized_funcs():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions

    return funcs

def test_app_function(tranquilized_funcs):
    app = make_app(tranquilized_funcs, 'cheese')
    assert len(app.blueprints) == 1

def test_two_app_functions(tranquilized_funcs):
    app = make_app(tranquilized_funcs, 'two_funcs')
    assert len(app.blueprints) == 1

def test_proxy_fix(tranquilized_funcs):
    app = make_app(tranquilized_funcs, 'cheese')
    assert isinstance(app.wsgi_app, ProxyFix)

def test_content_length(tranquilized_funcs):
    app = make_app(tranquilized_funcs, 'cheese', max_content_length=1024)
    assert app.config['MAX_CONTENT_LENGTH'] == 1024

def test_cors_star(tranquilized_funcs):
    app = make_app(tranquilized_funcs, 'cheese', origins='*')
    assert app.after_request_funcs

def test_secret_key(tranquilized_funcs):
    secret_key = 'tranquilizer'
    app = make_app(tranquilized_funcs, 'cheese', secret_key=secret_key)
    assert app.config['JWT_SECRET_KEY'] == secret_key

def test_projected_func_with_secret_key():
    here = dirname(__file__)
    fn = join(here, 'protected.py')
    script = ScriptHandler(fn)
    script.parse()
    tranquilized_funcs = script.tranquilized_functions

    secret_key = 'tranquilizer'
    app = make_app(tranquilized_funcs, 'cheese', secret_key=secret_key)
    assert app.config['JWT_SECRET_KEY'] == secret_key

def test_projected_func_without_secret_key():
    here = dirname(__file__)
    fn = join(here, 'protected.py')
    script = ScriptHandler(fn)
    script.parse()
    tranquilized_funcs = script.tranquilized_functions

    with pytest.raises(RuntimeError):
        app = make_app(tranquilized_funcs, 'cheese')
