'''construct flask-restx resources'''
from flask import jsonify
from flask_restx import Resource, reqparse
from collections.abc import Mapping, Sequence
from typing import List
from flask_jwt_extended import jwt_required

from .types import is_container, type_mapper


def make_parser(func_spec, location='args', compat=False):
    '''Create RequestParser from annotated function arguments

    arguments without default values are flagged as required

    Parameters
    ----------
    :param func_spec: The decorated functions spec
    :param location: expected location of arguments in request
                     'args', or 'body'
    :param compat: If compatibility with anaconda-enterprise-web-publisher
                   is required. (default: False)
    '''

    parser = reqparse.RequestParser(bundle_errors=True)
    for argument, spec in func_spec['args'].items():
        if compat and spec.get('annotation', None) is None:
            # un-typed arguments are returned to the
            # function as a list of strings by @publish
            action = 'append'
            _type = List[str]
        else:
            # @tranquilize assumes untyped
            # arguments are strings
            _type = spec.get('annotation', str)
            action = 'store'

        _default = spec.get('default', None)
        _type = type_mapper(_type)
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

        parser.add_argument(argument, type=_type,
                            default=_default,
                            required=(not ('default' in spec)),
                            location=_location,
                            action=action,
                            help=doc)

    return parser


def make_resource(func, api, requires_authentication=False):
    if func._methods:
        return _make_resources(func, api, requires_authentication=requires_authentication)
    else:
        return _make_resource(func, api, func._method, requires_authentication=requires_authentication)


def _make_resources(func, api, requires_authentication=False):
    '''Provide compatibility with web-publisher'''
    resources = {}
    for m in func._methods:
        resources[m] = getattr(_make_resource(func, api, m, requires_authentication), m)

    Tranquilized = type('Tranquilized', (Resource,), resources)

    return Tranquilized


def _make_resource(func, api, method, requires_authentication=False):
    location = 'form' if method in ['put','post'] else 'args'
    compat = True if (func._methods is not None) else False
    parser = make_parser(func._spec, location=location, compat=compat)

    @api.expect(parser, validate=True, strict=True)
    def _method(self):
        req = parser.parse_args()
        output = func(**req)
        return jsonify(output)

    error_docs = func._spec['error_docs']
    security = 'bearer_token' if requires_authentication else None
    _method = api.doc(responses=error_docs, security=security)(_method)

    if requires_authentication:
        _method = jwt_required()(_method)

    _method.__doc__ = func._spec['docstring']

    Tranquilized = type('Tranquilized', (Resource,), {method:_method})

    return Tranquilized

