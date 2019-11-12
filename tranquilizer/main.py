import sys
from os.path import dirname, basename
from argparse import ArgumentParser

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

    name = args.name if args.name else basename(args.filename)
    app = make_app(source.tranquilized_functions, name=name, prefix=args.prefix,
                   max_content_length=args.max_content_length)

    return app

def run():
    args = cli().parse_args()
    app = main(args)
    app.run(host=args.address, port=args.port,
            debug=args.debug)