from tranquilizer.main import cli, main, UnsupportedFileType
from tranquilizer.__init__ import __version__
from os.path import dirname, join
import pytest

def test_py():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn])
    main(args)

def test_ipynb():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.ipynb')
    args = cli().parse_args([fn])
    main(args)

def test_python():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.python')
    args = cli().parse_args([fn])
    with pytest.raises(UnsupportedFileType):
        main(args)

def test_name():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--name', 'cheese'])
    assert args.name == 'cheese'

def test_max_content_length():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--max_content_length', '1024'])
    assert args.max_content_length == 1024

def test_port():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--port', '5000'])
    assert args.port == 5000

def test_address():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--address', '127.0.0.1'])
    assert args.address == '127.0.0.1'

def test_url_prefix():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--prefix', 'python'])
    assert args.prefix == 'python'

def test_cors_arg():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--allow-origin', '*'])
    assert args.allow_origin == ['*']

def test_cors_args():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--allow-origin', 'localhost', '--allow-origin', '127.0.0.1'])
    assert args.allow_origin == ['localhost', '127.0.0.1']

def test_debug():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    args = cli().parse_args([fn, '--debug'])
    assert args.debug == True

def test_version():
    here = dirname(__file__)
    fn = join(here, 'cheese_shop.py')
    with pytest.raises(SystemExit):
        args = cli().parse_args([fn, '--version'])
        assert args.version == 'tranquilizer {}'.format(__version__)

def test_secret_key():
    here = dirname(__file__)
    fn = join(here, 'protected.py')
    args = cli().parse_args([fn, '--secret-key', 'tranquilizer'])
    assert args.secret_key == 'tranquilizer'
