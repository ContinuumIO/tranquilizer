from dateutil.parser import parse
from datetime import datetime
from typing import List, Generic, TypeVar
import base64
import numpy as np

T = TypeVar('T')
S = TypeVar('S')

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
    __schema__ = {'type':'string', 'format':'Anything accepted by dateutil.parser.parse()'}

    def __new__(cls, *args):
        if isinstance(args[0], str) and len(args)==1:
            return parse(args[0])
        else:
            return super().__new__(datetime, *args)

class TypedList(List, Generic[T]):
    '''An instantiable typed list

    This class supports specialization with [].

    fList = List[float]

    It will then attempt to convert elements of
    a list passed to the constructor

    list_of_floats = fList([0,1,2])'''
    def __new__(cls, *args, **kwds):
        _type = cls.__args__[0]
        _list = super().__new__(cls, *args, **kwds)

        return [_type(i) for i in _list]
