import inspect

from functools import wraps
from flask import g, request, redirect, url_for, flash
from flask_login import current_user

from src.modules.admission.admission_model import Admission


def query_params(f):
    """
    Decorator that will read the query parameters for the request.
    The below function_parameter_names are the names that are mapped (declared) in the function.
    """
    function_parameter_names = inspect.getargspec(f).args

    @wraps(f)
    def logic(*args, **kwargs):
        params = dict(kwargs)

        for param in function_parameter_names:
            # check if the functions' param is in the incoming request's parameters
            if param in request.args:
                params[param] = request.args.get(param)

        return f(**params)

    return logic
