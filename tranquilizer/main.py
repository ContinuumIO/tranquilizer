import sys
from os.path import dirname, basename
from argparse import ArgumentParser
from os import environ
import logging
from flask_jwt_extended import create_access_token

from .application import make_app
from .handler import ScriptHandler, NotebookHandler
from .__init__ import __version__


class UnsupportedFileType(Exception):
    pass

def cli():
    parser = ArgumentParser(prog="tranquilizer",
                            description="Put your functions to REST")
    parser.add_argument('filename', help='Script file with tranquilized functions')
    parser.add_argument('--name', help='Name of the REST API to use in Swagger')
    parser.add_argument('--max_content_length', type=int,
                        help='Maximum size of request in bytes for all endpoints')

    parser.add_argument('--port', '--anaconda-project-port', action='store', default=8086, type=int,
                        help='Port to listen on')
    parser.add_argument('--address', '--anaconda-project-address',
                        action='store',
                        default='0.0.0.0',
                        help='IP address the application should listen on.')
    parser.add_argument('--prefix','--anaconda-project-url-prefix', action='store', default='',
                        help='Prefix in front of urls')
    parser.add_argument('--allow-origin', action='append', type=str,
                        metavar = 'HOST[:PORT]',
                        help='Public hostnames which may connect to the endpoints')
    parser.add_argument('--secret-key', action='store', type=str, default=None,
                        help='Enable token authentication with the supplied key')

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Run API with debug output.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    # these anaconda-project arguments are ignored by Tranquilizer
    parser.add_argument('--anaconda-project-host', action='append', default=[],
                        help='Hostname to allow in requests')
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

    return parser


def main(args):
    sys.path.append(dirname(args.filename))

    extension = args.filename.split('.')[-1]
    if extension == 'py':
        source = ScriptHandler(args.filename)
    elif extension == 'ipynb':
        try:
            import nbconvert
        except ImportError as e: # pragma no cover
            raise ImportError("Please install nbconvert to serve Jupyter Notebooks.") from e

        source = NotebookHandler(args.filename)
    else:
        raise UnsupportedFileType('{} is not a script (.py) or notebook (.ipynb)'.format(args.filename))

    allow_origin_env = environ.get('TRANQUILIZER_ALLOW_ORIGIN')
    if allow_origin_env:
        origins = allow_origin_env.split(',')
    else:
        origins = args.allow_origin

    name = args.name if args.name else basename(args.filename)
    app = make_app(source.tranquilized_functions, name=name, prefix=args.prefix,
                   max_content_length=args.max_content_length, origins=origins,
                   secret_key=args.secret_key)

    return app

def run():
    args = cli().parse_args()
    app = main(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

        if args.allow_origin or environ.get('TRANQUILIZER_ALLOW_ORIGIN'):
            logging.getLogger('flask_cors').level = logging.DEBUG

    if args.secret_key:
        with app.app_context():
            token = create_access_token(identity='Tranquilized API user', expires_delta=False)
        print('-- This API secured with JWT using the HS256 algorithm. The following token can be used as an '
              ' Authorization Bearer token in the request header.')
        print()
        print(token)
        print()
        print('-- You can create more bearer tokens online at https://jwt.io using the secret-key you supplied '
              'on the command line.')

    app.run(host=args.address, port=args.port,
            debug=args.debug)