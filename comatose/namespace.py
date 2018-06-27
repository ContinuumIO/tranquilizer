'''construct flask-restplus blueprints'''
from flask import jsonify
from flask_restplus import Resource, Api, reqparse, Namespace
from argparse import ArgumentParser


def make_parser(func_spec):
    '''Create RequestParser from anotated function arguments

    arguments without default values are flagged as required'''

    parser = reqparse.RequestParser()
    for argument,spec in func_spec['args'].items():
        _type = spec.get('annotation', str)
        _default = spec.get('default', None)
        parser.add_argument(argument, type = _type, default = _default, required = (not _default))

    return parser

def make_api_namespace(func):
    api = Namespace(func._spec['name'], 'Comatose generated API for {}'.format(func._spec['name']))
    parser = make_parser(func._spec)

    @api.expect(parser, validate=True)
    def _method(self):
        '''{}'''.format(func._spec['docstring'])
        request = parser.parse_args()
        output = func(**request)
        return jsonify(output)

    methods = {mtd.lower():_method for mtd in func._methods}
    Comatose = type('Comatose', (Resource,), methods)

    api.add_resource(Comatose, '/')

    return api


