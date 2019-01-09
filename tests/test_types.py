import pytest

from tranquilizer import tranquilize
from tranquilizer.types import is_container, File, TextFile, Image, NDArray, ParsedDateTime, TypedList
from werkzeug.datastructures import FileStorage
import numpy as np

def test_is_container():
    l = [0,1,2]
    d = {'a':0, 'b':1}
    s = {0,1,1,2,3}
    
    for c in l,d,s:
        assert is_container(type(c)) == True
    
    f = 3.1415
    s = 'tranquilizer'
    i = 42

    for c in f,s,i:
        assert is_container(type(c)) == False

    # numpy arrays are sent as a single chunk of binary
    # data
    arr = np.array(l)
    assert is_container(type(arr)) == False


def test_is_container_custom():
    l = TypedList['str']
    assert is_container(l) == True

    for t in File, TextFile, Image, NDArray, ParsedDateTime:
        assert is_container(t) == False


def test_typed_list():


    integers = TypedList[int]
    assert integers('0') is 0
    
    with pytest.raises(ValueError):
        integers('a')
