import pytest

from tranquilizer.decorator import tranquilize, publish
from tranquilizer.types import File, TextFile, Image, NDArray
from tranquilizer.types import dt_factory, list_factory
from tranquilizer.types import is_container, is_list_subclass
from tranquilizer.types import type_mapper
from werkzeug.datastructures import FileStorage
import typing
import numpy as np
import datetime
import PIL.Image
import io
from os.path import join, dirname
import pandas as pd

def test_is_container():
    l = [0,1,2]
    d = {'a':0, 'b':1}
    
    for c in l,d:
        assert is_container(type(c)) == True
    
    f = 3.1415
    s = 'tranquilizer'
    i = 42

    for c in f,s,i:
        assert is_container(type(c)) == False
    
    assert is_container(typing.List) == True

    # numpy arrays are sent as a single chunk of binary
    # data
    arr = np.array(l)
    assert is_container(type(arr)) == False

def test_is_list_subclass():
    L = typing.List
    Li = typing.List[int]
    
    assert is_list_subclass(list) == True
    assert is_list_subclass(L) == True
    assert is_list_subclass(Li) == True

    assert is_list_subclass(int) == False
    assert is_list_subclass(str) == False

def test_list_factory():
    integers = list_factory(int)
    assert integers('0') is 0
    with pytest.raises(ValueError):
        integers('a')
        integers('3.14')

    floats = list_factory(float)
    assert np.isclose(floats('3.14'), 3.14)
    with pytest.raises(ValueError):
        floats('a')
    
    dates = list_factory(dt_factory(datetime.date))
    assert dates('2018-1-1 4 PM') == datetime.date(2018,1,1)

    assert not (integers == floats)

def test_dt_factory():
    d = dt_factory(datetime.date)
    assert d('2018-1-1 4 PM') == datetime.date(2018,1,1)

    dt = dt_factory(datetime.datetime)
    assert dt('2018-1-1 4 PM') == datetime.datetime(2018,1,1,16,0,0)

    ts = dt_factory(pd.Timestamp)
    assert ts('2018-1-1 4 PM') == datetime.datetime(2018,1,1,16,0,0)


def test_type_mapper_builtins():
    assert int is type_mapper(int)
    assert float is type_mapper(float)
    assert bool is type_mapper(bool)
    assert str is type_mapper(str)

def test_type_mapper_date():
    dm = type_mapper(datetime.date)
    df = dt_factory(datetime.date)
    assert dm('2018-1-1 4 PM') == df('2018-1-1 4 PM') == datetime.date(2018,1,1)

    dtm = type_mapper(datetime.datetime)
    dtf = dt_factory(datetime.datetime)
    assert dtm('2018-1-1 4 PM') == dtf('2018-1-1 4 PM') == datetime.datetime(2018,1,1,16,0,0)

def test_type_mapper_list():
    l1 = list_factory(int) 
    l2 = type_mapper(typing.List[int])
    assert l1('0') == l2('0') == 0

    l1 = list_factory(float) 
    l2 = type_mapper(typing.List[float])
    assert l1('3.14') == l2('3.14') == 3.14

    l1 = list_factory(str) 
    l2 = type_mapper(list)
    assert l1('a') == l2('a') == 'a'

    l1 = list_factory(str) 
    l2 = type_mapper(typing.List)
    assert l1('a') == l2('a') == 'a'

    l1 = list_factory(str) 
    l2 = type_mapper(typing.List[str])
    assert l1('a') == l2('a') == 'a'

    l1 = list_factory(bool) 
    l2 = type_mapper(typing.List[bool])
    assert l1('True') == l2('True') == True

    l1 = list_factory(dt_factory(datetime.date))
    l2 = type_mapper(typing.List[datetime.date])
    assert l1('2018-1-1 4 PM') == l2('2018-1-1 4 PM') == datetime.date(2018,1,1)

def test_type_mapper_files():
    assert type_mapper(typing.BinaryIO) is File
    assert type_mapper(typing.TextIO) is TextFile
    assert type_mapper(PIL.Image.Image) is Image
    assert type_mapper(np.ndarray) is NDArray

def test_binary_file():
    here = dirname(__file__)
    wf = FileStorage(filename=join(here,'file'))
    assert File(wf) is wf
    attrs = ['__location__', '__schema__', '__description__']
    assert all([hasattr(File, a) for a in attrs])

def test_text_file():
    here = dirname(__file__)
    wf = FileStorage(filename=join(here,'file'))
    tf = TextFile(wf)
    assert isinstance(tf, io.StringIO)
    attrs = ['__location__', '__schema__', '__description__']
    assert all([hasattr(TextFile, a) for a in attrs])

def test_array_file():
    here = dirname(__file__)
    wf = FileStorage(filename=join(here,'arr.npy'))
    nf = NDArray(wf.filename)
    assert isinstance(nf, np.ndarray)
    attrs = ['__location__', '__schema__', '__description__']
    assert all([hasattr(NDArray, a) for a in attrs])

def test_image_file():
    here = dirname(__file__)
    wf = FileStorage(filename=join(here,'kitty.jpg'))
    img = Image(wf.filename)
    assert isinstance(img, PIL.Image.Image)
    attrs = ['__location__', '__schema__', '__description__']
    assert all([hasattr(TextFile, a) for a in attrs])
    