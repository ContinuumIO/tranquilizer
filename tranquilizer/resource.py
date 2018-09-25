'''construct flask-restplus resources'''
from flask import jsonify, request
from flask_restplus import Resource, reqparse
from collections import Mapping, Sequence

from .types import is_container, type_mapper


def _make_parser(func_spec, location='args'):
    '''Create RequestParser from anotated function arguments

    arguments without default values are flagged as required'''

    parser = reqparse.RequestParser(bundle_errors=True)
    for argument,spec in func_spec['args'].items():
        _type = spec.get('annotation', str)
        _default = spec.get('default', None)
        action = 'store'

        _type = type_mapper(_type)

#       try:
#           description = getattr(_type, '__description__')
#       except AttributeError:
#           description = None

        doc = func_spec['param_docs'].get(argument, None)

        # Files (e.g., images) arrive in a different
        # Flask.Request location. The last value in
        # the tuple takes precedence.
        try:
            _loc = getattr(_type, '__location__')
            _location = (location, _loc)
        except AttributeError:
            _location = location


        if is_container(_type):
            action = 'append'
            type_name = _type.__args__[0].__name__
            _type.__schema__ = {'type':type_name}

        parser.add_argument(argument, type=_type,
                            default=_default,
                            required=(not _default),
                            location=_location,
                            action=action,
                            help=doc)

    return parser


def make_resource(func, api):
    location = 'form' if func._method == 'post' else 'args'
    parser = _make_parser(func._spec, location=location)

    @api.expect(parser, validate=True)
    def _method(self):
        request = parser.parse_args()
        output = func(**request)
        return jsonify(output)

    error_docs = func._spec['error_docs']
    if error_docs:
        _method = api.doc(responses = error_docs)(_method)

    _method.__doc__ = func._spec['docstring']

    Tranquilized = type('Tranquilized', (Resource,), {func._method:_method})

    return Tranquilized

