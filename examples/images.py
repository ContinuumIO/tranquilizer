
# curl -X POST -F "image=@<image-file>" http://localhost:8086/describe_image
# requests.post('http://localhost:8086/describe_image', files={'image':open('<image-file>', 'rb')})

from tranquilizer import tranquilize
from tranquilizer.types import Image
import numpy as np

@tranquilize(method='post')
def describe_image(image: Image):
    as_array = np.array(image)

    response = {
            'format':image.format,
            'shape': as_array.shape,
            'dtype': str(as_array.dtype)
    }

    return response
