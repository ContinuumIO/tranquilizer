from application import make_app, cli
from handler ...

def main():
    args = cli().parse_args()

    # collect namespaces from script

    app = make_app()
    app.run(host=args.anaconda_project_address, port=args.anaconda_project_port)

if __name__ == '__main__':
    main()
