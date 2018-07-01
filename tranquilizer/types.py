from collections import Mapping, Sequence
from dateutil.parser import parse
from datetime import datetime
from typing import List, Generic, TypeVar
from PIL import Image as pil_image
import io

T = TypeVar('T')
S = TypeVar('S')

def is_container(type_):
    '''Test if provided type function is a scalar

    strings and bytes are considered to be scalars.'''
    container = issubclass(type_, Sequence) or (issubclass(type_, Mapping))
    basic_scalars = issubclass(type_, str) or issubclass(type_, bytes)

    return  (not basic_scalars) and container


class Image(object):
    __location__ = 'files'
    def __new__(cls, file):
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        return pil_image.open(in_memory_file)


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

