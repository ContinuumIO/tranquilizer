from tranquilizer.application import make_app
from tranquilizer.handler import ScriptHandler
from werkzeug.middleware.proxy_fix import ProxyFix
from os.path import dirname, join

def test_app_function():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions

    app = make_app(funcs, 'cheese')
    assert len(app.blueprints) == 1

def test_app_function():
    here = dirname(__file__)
    fn = join(here, 'two_funcs.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions

    app = make_app(funcs, 'two_funcs')
    assert len(app.blueprints) == 1

def test_proxy_fix():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions

    app = make_app(funcs, 'cheese')
    assert isinstance(app.wsgi_app, ProxyFix)

def test_content_length():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions

    app = make_app(funcs, 'cheese', max_content_length=1024)
    assert app.config['MAX_CONTENT_LENGTH'] == 1024