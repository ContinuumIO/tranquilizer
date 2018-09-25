from collections import Mapping, Sequence
from dateutil.parser import parse
from datetime import datetime, date
from typing import List, Generic, TypeVar, TextIO, BinaryIO
from werkzeug.datastructures import FileStorage
from PIL import Image as pil_image
import numpy as np
import io

T = TypeVar('T')
S = TypeVar('S')

def is_container(type_):
    '''Test if provided type function is a scalar

    strings and bytes are considered to be scalars.'''
    container = issubclass(type_, Sequence) or (issubclass(type_, Mapping))
    basic_scalars = issubclass(type_, str) or issubclass(type_, bytes)

    return  (not basic_scalars) and container


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
        f = super().__new__(cls, *args, **kwargs)
        return pil_image.open(f)


class NDArray(File):
    '''Returns a NumPy array using np.load()'''
    __schema__ = {'type':'file', 'format':'NumPy array'}
    __description__ = 'NumPy array file.'
    def __new__(cls, *args, **kwargs):
        f = super().__new__(cls, *args, **kwargs)
        return np.load(f)


class ParsedDateTime(Generic[T]):
    '''A flexible dateteime.datetime class

    recieves a string: use dateutil to parse
    
    The type specifier determines the returned type.
    ParsedDateTime[datetime.date]
    ParsedDateTime[datetime.datetime]
    ParsedDateTime[pd.Timestamp]
    '''
    __schema__ = {'type':'string', 'format':'date-time'}
    __description__ = 'dateutil.parser.parse compatible datetime string'

    def __new__(cls, *args):
        parsed =  parse(args[0])
        _type = cls.__args__[0]
        if issubclass(_type, date):
            return parsed.date()
        else:
            return _type(parsed)
        return parsed


class TypedList(List, Generic[T]):
    '''An dummy typed list

    This class supports specialization with [].

    fList = List[float]

    It is expected to only receive one input.'''
    __schema__ = {'type':'string'}

    def __new__(cls, *args, **kwds):
        _type = cls.__args__[0]
        return _type(*args)


def type_mapper(type_):
    '''Map common type hints to custom classes
    
    If no conversion is necessary the input type
    is returned.
    '''

    if issubclass(type_, List):
        try:
            item_type = type_.__args__[0]
        except:
            item_type = str
        return TypedList[item_type]
    elif issubclass(type_, TextIO):
        return TextFile
    elif issubclass(type_, BinaryIO):
        return File
    elif issubclass(type_, pil_image.Image):
        return Image
    elif issubclass(type_, np.ndarray):
        return NDArray
    elif issubclass(type_, (datetime, date)):
        return ParsedDateTime[type_]
    else:
        return type_