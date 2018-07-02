from tranquilizer import tranquilize
from tranquilizer.types import TextFile, NDArray
import numpy as np

@tranquilize('post')
def text_file(file: TextFile):
    return {'response':file.read()}

@tranquilize('post')
def array_file(arr: NDArray):
    return {'response':(arr.shape, str(arr.dtype))}
