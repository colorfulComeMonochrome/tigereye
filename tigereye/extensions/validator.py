import functools

from flask import request, jsonify
from tigereye.helper.code import Code


class Validator(object):
    def __init__(self, **parameter_template):
        self.pt = parameter_template

    def __call__(self, f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                request.params = {}
                for k, v in self.pt.items():
                    request.params[k] = v(request.values[k])
            except Exception:
                response = jsonify(
                    rc=Code.required_parameter_missing.value,
                    msg=Code.required_parameter_missing.name,
                    data={'require_param': k}
                )
                response.status_code = 400
                return response
            return f(*args, **kwargs)
        return decorated_function


def multi_int(values):
    return [int(i) for i in values.split(',')]


