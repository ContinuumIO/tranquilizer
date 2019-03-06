import sys
from os.path import dirname, basename

from .application import make_app, cli
from .handler import ScriptHandler, NotebookHandler

class UnsupportedFileType(Exception):
    pass

def main():
    args = cli().parse_args()
    sys.path.append(dirname(args.filename))

    extension = args.filename.split('.')[-1]
    if extension == 'py':
        source = ScriptHandler(args.filename)
    elif extension == 'ipynb':
        source = NotebookHandler(args.filename)
    else:
        raise UnsupportedFileType('{} is not a script (.py) or notebook (.ipynb)'.format(args.filename))

    name = args.name if args.name else basename(args.filename)
    app = make_app(source.tranquilized_functions, name=name, prefix=args.prefix,
            max_content_length=args.max_content_length)

    app.run(host=args.address, port=args.port,
            debug=args.debug)

if __name__ == '__main__':
    main()
