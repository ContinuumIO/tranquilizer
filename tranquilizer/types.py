from collections.abc import Mapping, Sequence
from dateutil.parser import parse
from datetime import datetime, date
from typing import TextIO, BinaryIO
from werkzeug.datastructures import FileStorage
from flask_restx.reqparse import PY_TYPES
from flask_restx import fields
import io

def is_container(type_):
    '''Test if provided type function is a scalar

    strings and bytes are considered to be scalars.'''

    origin = getattr(type_, '__origin__', None)
    if origin is not None:
        # Due to PEP560 we need to handle new typing
        # classes carefully
        return issubclass(type_.__origin__, Sequence)

    container = issubclass(type_, Sequence) or (issubclass(type_, Mapping))
    basic_scalars = issubclass(type_, str) or issubclass(type_, bytes)

    return (not basic_scalars) and container


def is_list_subclass(type_):
    origin = getattr(type_, '__origin__', None)
    if origin is not None:
        return issubclass(type_.__origin__, list)
    else:
        return issubclass(type_, list)


class File(FileStorage):
    '''Thin wrapper for werkzeug.datastructures.FileStorage'''
    __location__ = 'files'
    __schema__ = {'type':'file', 'format':'binary file'}
    __description__ = 'Read file as binary.'
    def __new__(cls, file):
        return file


class TextFile(File):
    '''Returns io.StringIO object'''
    __schema__ = {'type':'file', 'format':'text file'}
    __description__ = 'Read file as text.'
    def __new__(cls, *args, **kwargs):
        f = super().__new__(cls, *args, **kwargs)
        t = io.StringIO(f.read().decode())
        return t


class Image(File):
    '''Returns PIL.Image object'''
    __schema__ = {'type':'file', 'format':'image'}
    __description__ = 'Read image file as PIL.Image.'
    def __new__(cls, *args, **kwargs):
        try:
            from PIL import Image as pil_image
        except ImportError as e: # pragma: no cover
            e.args = ("Please install pillow to define an image type.",)
            raise e
        f = super().__new__(cls, *args, **kwargs)

        return pil_image.open(f)


class NDArray(File):
    '''Returns a NumPy array using np.load()'''
    __schema__ = {'type':'file', 'format':'NumPy array'}
    __description__ = 'NumPy array file.'
    def __new__(cls, *args, **kwargs):
        try:
            import numpy as np
        except ImportError as e: # pragma: no cover
            e.args = ("Please install NumPy to define an array type.",)
            raise e
        f = super().__new__(cls, *args, **kwargs)
        return np.load(f)

def dt_factory(type_):
    class ParsedDatetime(type):
        '''A flexible datetime class

        receives a string returns datetime object
        '''
        __schema__ = {'type': 'string'}
        __description__ = 'dateutil.parser.parse compatible datetime string'
        def __new__(self, arg):
            if type_ is datetime:
                return parse(arg)
            elif type_ is date:
                return parse(arg).date()
            else:
                # most commonly used for pd.TimeStamp.
                # any method that can take a string
                return type_(arg)

    return ParsedDatetime


def list_factory(type_):
    items = getattr(type_, '__schema__', {}).get('type', PY_TYPES.get(type_, 'string'))

    class TypedList(Sequence):
        # using append with flask-restx
        # means that list is constructed later
        __schema__ = {'type': items}
        __description__ = 'List with values of type {}'.format(items)
        def __new__(cls, arg):
            return type_(arg)
        
    return TypedList


def type_mapper(type_):
    '''Map common type hints to custom classes

    If no conversion is necessary the input type
    is returned.
    '''

    try:
        from PIL import Image as pil_image
        has_pil_image = True
    except ImportError: # pragma: no cover 
        has_pil_image = False

    try:
        import numpy as np
        has_numpy = True
    except ImportError: # pragma: no cover 
        has_numpy = False

    if is_list_subclass(type_):
        try:
            item_type = type_.__args__[0]
            if issubclass(item_type, (datetime, date)):
                item_type = dt_factory(item_type)
        except (AttributeError, TypeError):
            item_type = str
        return list_factory(item_type)
    elif issubclass(type_, TextIO):
        return TextFile
    elif issubclass(type_, BinaryIO):
        return File
    elif issubclass(type_, (datetime, date)):
        return dt_factory(type_)
    elif has_pil_image and issubclass(type_, pil_image.Image):
        return Image
    elif has_numpy and issubclass(type_, np.ndarray):
        return NDArray
    else:
        return type_
