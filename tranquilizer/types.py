from collections import Mapping, Sequence
from dateutil.parser import parse
from datetime import datetime
from typing import List, Generic, TypeVar
import base64
import numpy as np
import io
from PIL import Image as pil_image

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


class Bytes(bytes, Generic[T]):
    '''Base Class for byte string with custom decoding'''
    def __new__(cls, utf8_string):
        decoder = cls.__args__[0]
        # the kernelgateway always sends UFT8 strings
        return decoder(utf8_string.encode())


Base64Bytes = Bytes[base64.decodebytes]


class NDArray(Base64Bytes, Generic[T]):
    '''NumPy arrays as base64 byte string'''
    def __new__(cls, utf8_string):
        dtype = cls.__args__[0]

        _bytes = super().__new__(Base64Bytes, utf8_string)
        return np.fromstring(_bytes, dtype=dtype)


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

