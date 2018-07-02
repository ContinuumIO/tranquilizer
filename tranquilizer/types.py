from collections import Mapping, Sequence
from dateutil.parser import parse
from datetime import datetime
from typing import List, Generic, TypeVar
from werkzeug.datastructures import FileStorage
from PIL import Image as pil_image
import numpy as np
import io

__all__ = ['File', 'TextFile', 'Image', 'NDArray',
           'ParsedDateTime', 'TypedList'
]

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


class ParsedDateTime(datetime):
    '''A flexible dateteime.datetime class

    If the constructor

    recieves a string: use dateutil to parse
    receives an integer: use datetime.datetime'''
    __schema__ = {'type':'string', 'format':'date-time'}
    __description__ = 'dateutil.parser.parse compatible datetime string'

    def __new__(cls, *args):
        if isinstance(args[0], str) and len(args)==1:
            return parse(args[0])
        else:
            return super().__new__(datetime, *args)


class TypedList(List, Generic[T]):
    '''An dummy typed list

    This class supports specialization with [].

    fList = List[float]

    It is expected to only receive one input.'''
    __schema__ = {'type':'string'}

    def __new__(cls, *args, **kwds):
        _type = cls.__args__[0]
        return _type(*args)
