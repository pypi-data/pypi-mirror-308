from functools import wraps
from pymdgen import getargspec  # Import your __init__.py module


def test_getargspec_simple_function():
    def my_function(a, b, c=10):
        pass

    expected_result = [
        ["a", "b", "c"],
        None,
        None,
        [
            10,
        ],
    ]
    assert getargspec(my_function) == expected_result


def test_getargspec_args_kwargs():
    def my_function(a, b, *args, **kwargs):
        pass

    expected_result = [
        ["a", "b", "args", "kwargs"],
        None,
        None,
        [],
    ]
    assert getargspec(my_function) == expected_result


def test_getargspec_decorated_function():
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @my_decorator
    def my_function(a, b, c=20):
        pass

    expected_result = [
        ["a", "b", "c"],
        None,
        None,
        [
            20,
        ],
    ]
    assert getargspec(my_function) == expected_result
