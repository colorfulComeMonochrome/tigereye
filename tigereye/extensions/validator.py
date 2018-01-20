import functools
from flask import request, jsonify
from tigereye.helper.code import Code


class Validator(object):
    def __init__(self, **parameter_template):
        self.pt = parameter_template

    # 类的实例化对象可以被当做函数调用，当调用时执行call函数
    def __call__(self, f):
        # 不使用functools.wraps这个方法的话,被装饰函数的名字会变成装饰器的函数名，且无法调用函数的__doc__方法
        @functools.wraps(f)
        # 函数参数是被装饰函数传入的所有参数
        def decorated_function(*args, **kwargs):
            try:
                # 创建自定义参数字典
                request.params = {}
                # 从传入装饰器的所有关键字参数中拿到键->k,值->v
                # 例: 传入装饰器cid=int    传入request   cid=cid1
                # k: cid    v: int
                for k, v in self.pt.items():
                    # 结果为:     cid: int(cid1)
                    # 进行强制类型转换,成功表示类型符合条件,直接返回response
                    # 失败执行except
                    request.params[k] = v(request.values[k])
            except Exception:
                # 返回 缺少必要参数 状态码
                response = jsonify(
                    rc=Code.required_parameter_missing.value,
                    msg=Code.required_parameter_missing.name,
                    data={'require_param': k}
                )
                response.status_code = 400
                return response
            # 成功继续调用被装饰的函数,此处的f指的是call函数中座位参数传入的函数
            return f(*args, **kwargs)

        return decorated_function


class ValidationError(Exception):
    def __init__(self, message, values):
        super().__init__(message)
        self.values = values


def multi_int(values):
    return [int(i) for i in values.split(',')]


def complex_int(values, sperator='-'):
    """1-200-5000"""
    digits = values.split(sperator)
    result = []
    for digit in digits:
        if not digit.isdigit():
            raise ValidationError('complex int error: %s' % values, values)
        result.append(int(digit))
    return result


def multi_complex_int(values, sperator=','):
    """1-200-5000,2-200-5000"""
    return [complex_int(i) for i in values.split(sperator)]
