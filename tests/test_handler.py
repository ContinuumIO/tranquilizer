from tranquilizer.handler import ScriptHandler, NotebookHandler
from os.path import dirname, join

def test_script_handler():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    assert script.fn == fn

def test_script_parser():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    script.parse()
    assert [hasattr(script, attr) for attr in ['modules','nodes']]

def test_nb_handler():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.ipynb')
    nb = NotebookHandler(fn)
    assert nb.fn == fn

def test_nb_parser():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.ipynb')
    nb = NotebookHandler(fn)
    nb.parse()
    assert [hasattr(nb, attr) for attr in ['modules','nodes']]

def test_tranquilized_script():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions
    assert len(funcs) == 1

def test_tranquilized_nb():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.ipynb')
    nb = NotebookHandler(fn)
    nb.parse()
    funcs = nb.tranquilized_functions
    assert len(funcs) == 1

def test_published_script():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop_publish.py')
    script = ScriptHandler(fn)
    script.parse()
    funcs = script.tranquilized_functions
    assert len(funcs) == 1