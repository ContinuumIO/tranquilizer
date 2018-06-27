from argparse import ArugmentParser
from application import make_app

def cli():
    # arg parser for the standard anaconda-project options
    parser = ArgumentParser(prog="api",
                            description="Serve API from script file")
    parser.add_argument('filename', help='File with published functions', type=argparse.FileType('r'))
    parser.add_argument('--anaconda-project-host', action='append', default=[],
                        help='Hostname to allow in requests')
    parser.add_argument('--anaconda-project-port', action='store', default=8086, type=int,
                        help='Port to listen on')
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
    parser.add_argument('--anaconda-project-url-prefix', action='store', default='',
                        help='Prefix in front of urls')
    parser.add_argument('--anaconda-project-address',
                        action='store',
                        default='0.0.0.0',
                        help='IP address the application should listen on.')

    return parser

def main():
    args = cli().parse_args()

    ## read and execute filename

    app.run(host=args.anaconda_project_address, port=args.anaconda_project_port)
