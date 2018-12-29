import sys
from os.path import dirname, basename

from .application import make_app, cli
from .handler import get_tranquilized_functions

def main():
    args = cli().parse_args()
    sys.path.append(dirname(args.filename))

    functions = get_tranquilized_functions(args.filename)

    name = args.name if args.name else basename(args.filename)
    app = make_app(functions, name=name, prefix=args.anaconda_project_url_prefix)

    app.run(host=args.anaconda_project_address, port=args.anaconda_project_port,
            debug=args.debug)

if __name__ == '__main__':
    main()
