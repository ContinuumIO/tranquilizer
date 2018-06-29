'''construct flask-restplus resources'''
from flask import jsonify, request
from flask_restplus import Resource, reqparse
from collections import Mapping, Sequence

from .types import is_container

def _make_parser(func_spec, location='args'):
    '''Create RequestParser from anotated function arguments

    arguments without default values are flagged as required'''

    parser = reqparse.RequestParser()
    for argument,spec in func_spec['args'].items():
        _type = spec.get('annotation', str)
        _default = spec.get('default', None)
        action = 'append' if is_container(_type) else 'store'

        parser.add_argument(argument, type=_type,
                            default=_default,
                            required=(not _default),
                            location=location,
                            action=action)

    return parser


def make_resource(func, api):
    location = 'form' if func._method == 'post' else 'args'
    parser = _make_parser(func._spec, location=location)

    @api.expect(parser, validate=True)
    def _method(self):
        request = parser.parse_args()
        output = func(**request)
        return jsonify(output)

    _method.__doc__ = func.__doc__

    Tranquilized = type('Tranquilized', (Resource,), {func._method:_method})

    return Tranquilized

