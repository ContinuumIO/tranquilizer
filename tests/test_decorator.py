from tranquilizer import tranquilize

def test_attributes():
    
    def _func():
        return 0
    
    decorated = tranquilize()(_func)

    assert hasattr(decorated, '_spec')
    assert hasattr(decorated, '_method')


def test_method():

    # separate functions are used for
    # get and post. Calling the decorator
    # a second time updates the original
    # function
    def _funcg():
        return 0

    get = tranquilize(method='GET')(_funcg)
    assert get._method == 'get'

    def _funcp():
        return 0

    post = tranquilize(method='PosT')(_funcp)
    assert post._method == 'post'


def test_spec():

    def _func():
        return 0

    decorated = tranquilize()(_func)
    assert isinstance(decorated._spec, dict)
    assert decorated._spec.keys() == set(['name','docstring','args', 'param_docs', 'error_docs'])