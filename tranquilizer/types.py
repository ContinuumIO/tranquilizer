from collections import Mapping, Sequence
from dateutil.parser import parse
from datetime import datetime, date
from typing import TextIO, BinaryIO
from werkzeug.datastructures import FileStorage
import io

def is_container(type_):
    '''Test if provided type function is a scalar

    strings and bytes are considered to be scalars.'''

    if hasattr(type_, '__origin__'):
        # Due to PEP560 we need to handle new typing
        # classes carefully
        return issubclass(type_.__origin__, Sequence)

    container = issubclass(type_, Sequence) or (issubclass(type_, Mapping))
    basic_scalars = issubclass(type_, str) or issubclass(type_, bytes)

    return  (not basic_scalars) and container


def is_list_subclass(type_):
    if hasattr(type_, '__origin__'):
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
        except ImportError as e:
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
        except ImportError as e:
            e.args = ("Please install NumPy to define an array type.",)
            raise e
        f = super().__new__(cls, *args, **kwargs)
        return np.load(f)


def dt_factory(type_):
    class ParsedDatetime(object):
        '''A flexible dateteime.datetime class

        receives a string returns datetime object
        '''
        __schema__ = {'type':'string', 'format':'date-time'}
        __description__ = 'dateutil.parser.parse compatible datetime string'
        def __new__(cls, *args):
            parsed =  parse(args[0])
            if issubclass(type_, date):
                return parsed.date()
            else:
                return type_(parsed)
            return parsed
    return ParsedDatetime


def list_factory(type_):
    # helps with List[datetime] usage
    type_ = type_mapper(type_)
    class TypedList(Sequence):
        # using append with flask-restplus
        # means that list is constructed later

        def __new__(cls, arg):
            if hasattr(type_, '__schema__'):
                cls.__schema__ = type_.__schema__
            else:
                cls.__schema__ = {'type':type_.__name__}
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
    except ImportError:
        has_pil_image = False

    try:
        import numpy as np
        has_numpy = True
    except ImportError:
        has_numpy = False

    if is_list_subclass(type_):
        try:
            item_type = type_.__args__[0]
        except:
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
