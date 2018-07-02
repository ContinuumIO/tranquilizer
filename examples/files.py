# curl -X POST -F "file=@<text-file>" http://localhost:8086/text_file
# requests.post('http://localhost:8086/text_file', files={'file':open('<text-file>', 'rb')})


# curl -X POST -F "arr=@<array-file.npy>" http://localhost:8086/array_file
# requests.post('http://localhost:8086/array_file', files={'arr':open('<np-array-file.npy>', 'rb')})
# f = BytesIO()
# np.save(f, arr)
# requests.post('http://localhost:8086/array_file', files={'arr':f.getvalue()})

from tranquilizer import tranquilize
from tranquilizer.types import TextFile, NDArray
import numpy as np

@tranquilize('post')
def text_file(file: TextFile):
    return {'response':file.read()}

@tranquilize('post')
def array_file(arr: NDArray):
    return {'response':(arr.shape, str(arr.dtype))}
