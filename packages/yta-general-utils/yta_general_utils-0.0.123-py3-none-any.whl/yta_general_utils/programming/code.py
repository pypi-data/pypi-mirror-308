"""
    # TODO: I don't know if this is the best name for this
    kind of code, but here it is.

    Maybe it should be with the code in 'parameter_obtainer.py'
    as it is such a dynamic way of interact with the code.
    Feel free to change it in the future for a more intuitive
    location.
"""
from yta_general_utils.programming.parameter_validator import PythonValidator
import inspect


# 'f.__qualname__' is very interesting thing as it works
# with the full path, not as 'f.__name__' does, this is
# one example of it value when doing it from a local file:
#
# 'Example.example.__qualname__'
# test_discord_video.<locals>.Example.example
#
# And yes, the 'example' is a @staticmethod defined in the
# Example class that is contained in the 'test_discord_video'
# file

def is_class_staticmethod(cls: type, method: 'function'):
    """
    Check if the provided 'method' is an staticmethod (a
    function) defined in the also provided 'cls' class.
    """
    if not PythonValidator.is_a_class(cls):
        raise Exception('The provided "cls" parameter is not a class.')
    
    if not PythonValidator.is_a_function(method):
        raise Exception('The provided "method" parameter is not a function.')
    
    for function in inspect.getmembers(cls, predicate = inspect.isfunction):
        if function[0] == method.__name__:
            return True
        
    return False