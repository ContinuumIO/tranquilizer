# Tranquilizer

Deploy a REST API with one line by decorating your functions.

## Install

The package is available for all Mac, Linux, and Windows on my conda channel. Python 2 is not supported.

```
> conda install -c conda-forge tranquilizer
```

## Quick start

Tranquilizer can be used with either Jupyter Notebooks (`.ipynb`) or Python script files (`.py`).

The decorated function below will be served as an end point called `order` with the GET method. The
function must return a JSON serializable object.

See the [complete description of `@tranquilize()`](#tranquilize-decorator) below.

```python
from tranquilizer import tranquilize

@tranquilize()
def order(cheese):
    '''I'd like to buy some cheese!'''
    return "I'm afraid we're fresh out of {}, Sir.".format(cheese)
```

The REST API is served by [Flask](https://flask.palletsprojects.com) and [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
using the `tranquilizer` command.


```
> tranquilizer cheese_shop.ipynb
 * Serving Flask app "tranquilizer.application" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8086/ (Press CTRL+C to quit)

```

Let's see if there is any Red Leicester.

```
> curl -G http://localhost:8086/order --data-urlencode "cheese=Red Leicester"
"I'm afraid we're fresh out of Red Leicester, Sir."
```

or using the Requests library in Python.

```python
In [1]: import requests

In [2]: response = requests.get('http://localhost:8086/order', params={'cheese':'Red Leicester'})

In [3]: response.text
Out[3]: '"I\'m afraid we\'re fresh out of cheddar, Sir."\n'
```

The *tranquilized* API is documented with [Swagger](https://swagger.io/tools/open-source/) and is accessible
in your web browser at [http://localhost:8086](http://localhost:8086).

![](https://raw.githubusercontent.com/ContinuumIO/tranquilizer/9b4a738d1f24af7f4c2397d43454e0fe2ee5e86b/img/swagger.png)

## Tranquilize Decorator

The `@tranqulize` decorator will assign the GET method by default. POST is also supported with `method='post'`.
Other methods are under consideration.

By default a *tranquilized* function will receive all inputs as strings. This behavior can be modified by using [type hints](https://docs.python.org/3/library/typing.html). When data is received by the Flask server it will use the provided
type function to transform the string to the requested data type. This avoids having to perform the conversion in your *tranquilized* function.

## Supported source formats

Tranquilizer can serve functions written in Python source (`.py`) files or Jupyter Notebooks (`.ipynb`).

When working interactively in Jupyter Notebooks the decorated functions will continue to operate as normal.
Note that all calls to [Jupyter Magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
and Shell (`!`) commands will be ignored when the REST API is served.
Only those lines will be ignored, the rest of the cell will continue to run.

## Data Types

In addition to [*builtin* types](https://docs.python.org/3/library/stdtypes.html) Tranquilizer 
provides specialized support for Lists, date/datetime, and files. 


|Type|Description|
|----|-----------|
|`datetime.date` or `datetime.datetime`| Converts string with `dateutil.parser.parse` and returns specified type.|
|`list`| Converts *repeated* arguments to a list of strings.|
|`typing.List[<type>]`| Converts *repeated* arguments to a list; each value is converted to `<type>`.|

`List` arguments are constructed using the `action='append'` argument described in
the [Flask RESTX documentation](https://flask-restx.readthedocs.io/en/stable/parsing.html#multiple-values-lists).
Any valid type can be used in `List[]`.

The following file-like types are handled by [werkzeug `FileStorage`](http://werkzeug.pocoo.org/docs/0.14/datastructures/#werkzeug.datastructures.FileStorage).
`FileStorage` is a file-like object that supports methods like `.read()` and `.readlines()`.
These types support sending files with cURL using `-F`.

|Type|Description|
|----|-----------|
|`typing.BinaryIO`| File-like object to read binary data.|
|`typing.TextIO`| Converts `FileStorage` type to `io.StringIO()`.|

Further, specific support for Image and NumPy files are provided. The binary contents of the file are automatically converted.

|Type|Description|
|----|-----------|
|`PIL.Image.Image`| Converts `FileStorage` type to PIL Image.|
|`numpy.ndarray`| Converts `FileStorage` type to NumPy array using `np.load()`. |

### Custom types

Custom type classes can be built...

## Type hints example

The example below uses `int`, `datetime.datetime`, and `typing.List`. `datetime.datetime` support
has been built with `datetutil` and will convert any compatible datetime string to a `datetime.datetime` object. `typing.List`
supports specialization with `[]` and will transform all *repeated* arguments passed to the REST API into a list and convert
the type of each element.

Finally, tranquilizer supports default arguments.

```python
from tranquilizer import tranquilize
from datetime import date
from typing import List

@tranquilize(method='post')
def convert(string: str, date: date, items: List[float], factor: int = 10):
    '''Let's convert strings to something useful'''

    new_items = [i * factor for i in items]

    response = {
            'string': string.upper(),
            'date'  : date.strftime('%c'),
            'items' : new_items
    }

    return response
```

Let's see what happens when I POST to this REST API.

```python
In [1]: data = {'string':'hello, world!', 'date':'4th July 1776', 'items':range(5)}

In [2]: import requests

In [3]: response = requests.post('http://localhost:8086/convert', data=data)

In [4]: response.json()
Out[4]:
{'date': 'Thu Jul  4 00:00:00 1776',
 'items': [0.0, 10.0, 20.0, 30.0, 40.0],
 'string': 'HELLO, WORLD!'}

In [5]:
```

## Securing the API with a bearer token

If you need to secure your tranquilized API with an Authorization Bearer token use the `--secret-key` command-line
flag. The supplied secret key is used to decrypt JWT tokens. When the tranquilizer server starts a bearer token
is printed to standard out that can be used to access the API. Here's an example of the output.

NOTE: It is important that you keep your secret key safe and not share it as it is used to sign and verify bearer
tokens, not to access the API.

```
> tranquilizer --secret-key <secret-key> cheese_shop.ipynb
-- This API secured with JWT using the HS256 algorithm. The following token can be used as an  Authorization Bearer token in the request header.

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzODc0MzkxNiwianRpIjoiNGY0YTdiZWYtMWJiZi00ZGUwLWI0MDMtOTVhNzY2Y2IxNWUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlRyYW5xdWlsaXplZCBBUEkgdXNlciIsIm5iZiI6MTYzODc0MzkxNn0.pWoKvH_N9abFUYLzbzc02ewnPGPbvTjiFAVI3GlVltw

-- You can create more bearer tokens online at https://jwt.io using the secret-key you supplied on the command line.
 * Serving Flask app "tranquilizer.application" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8086/ (Press CTRL+C to quit)
```

A user can then utilize the supplied token in requests to the API, for example with curl

```
> TOKEN='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzODc0MzkxNiwianRpIjoiNGY0YTdiZWYtMWJiZi00ZGUwLWI0MDMtOTVhNzY2Y2IxNWUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlRyYW5xdWlsaXplZCBBUEkgdXNlciIsIm5iZiI6MTYzODc0MzkxNn0.pWoKvH_N9abFUYLzbzc02ewnPGPbvTjiFAVI3GlVltw'
> curl -H 'Authorization: Bearer ${TOKEN}' http://localhost:8086/order?cheese=cheddar
"I'm afraid we're fresh out of cheddar, Sir."
```

If the authorization header is not included in the request a 401 error is returned.

```
> curl -i http://localhost:8086/order?cheese=cheddar
HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/1.0.1 Python/3.7.9
Date: Mon, 06 Dec 2021 15:46:19 GMT

{"message":"Missing Authorization Header"}
```

### Choosing functions to protect with authentication

By default all `@tranquilize()` decorated functions will require authentication when using the `--secret-key` command
line argument. To disable authentication for specific functions use the `requires_authentication=False` keyword
argument. For example in the tranquilized functions below the `cheeses()` function does not require the
`Authorization: Bearer ${TOKEN}` header, but the `order()` function does require the header.

When `requires_authentication=None` or is not included in the decorator call the function will require authentication
when using the `--secret-key` CLI argument. If `requires_authentication=True` is used but tranquilizer is not started
with the `--secret-key` argument a `RuntimeError` exception is raised.


```python
from tranquilizer import tranquilize

@tranquilize()
def cheeses(method='get', requires_authentication=False):
    '''List the available cheeses'''

    return ['Red Leicester', 'Tilsit', 'Caerphilly', 'Bel Paese', 'Venezuelan Beaver Cheese']

@tranquilize(method='post')
def order(cheese):
    '''I'd like to buy some cheese!'''
    return "I'm afraid we're fresh out of {}, Sir.".format(cheese)
```

### Swagger

When using `--set-secret` and the optional `requires_authentication` keyword argument the Swagger docs
are still accessible but in order to *try out* an endpoint that requires authentication you must first
click the `Authorize` button at the top right. In the dialog box include the bearer token prepended by `Bearer`
as shown in the screenshot. 

![](img/swagger_authorize.png)