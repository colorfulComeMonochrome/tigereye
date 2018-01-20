from unittest import TestCase
from urllib.parse import urlencode

from flask import json
import tigereye
from tigereye.configs.test import TestConfig
from tigereye.helper.code import Code


class FlaskTestCase(TestCase):
    def setUp(self):
        app = tigereye.create_app(TestConfig)
        app.logger.disabled = True
        self.app = app.test_client()
        with app.app_context():
            from tigereye.models import db
            from tigereye.models.cinema import Cinema
            from tigereye.models.hall import Hall
            from tigereye.models.movie import Movie
            from tigereye.models.play import Play
            from tigereye.models.seat import PlaySeat, Seat
            from tigereye.models.order import Order
            db.create_all()
            Cinema.create_test_data(cinema_num=1, hall_num=3, play_num=3)
            # Cinema.create_test_data()
            Movie.create_test_data()

    # get或者post方法的断言测试
    # 此函数代替api中的函数发送get/post请求,封装请求过程,加快开发效率
    # 参数: uri 请求的相对路径   assertcode 请求发送返回的状态码,默认为200表示请求成功
    # 参数: method 规定请求方式为get还是post     **params 表示api发送的多个参数
    def assert_get(self, uri, assertcode=200, method='GET', **params):
        if method == 'POST':
            # response value
            # 向uri表示的路径发送post请求,请求所带参数为params
            rv = self.app.post(uri, data=params)
        # 发送get请求
        else:
            # 如果请求有参数
            if params:
                # 将参数拼到uri路径后      例: /cinema/get/?pid=1  urlencode工具:将传入的参数都变成get参数格式
                # print(urlencode(params))  结果:sid=2&pid=1
                rv = self.app.get('%s?%s' % (uri, urlencode(params)))
            else:
                # 没有参数直接请求uri
                rv = self.app.get(uri)
        # assertEqual 断言  比较传入的两个参数，如果相等则继续运行，不相等则返回fail
        self.assertEqual(rv.status_code, assertcode)
        return rv

    # 测试网络请求返回值是否为200,即测试请求是否成功
    def get200(self, uri, method='GET', **params):
        return self.assert_get(uri, 200, method, **params)

    # 获取请求回来的response对象，并将其转化为json格式
    def get_json(self, uri, method='GET', **params):
        # 从get200中获取返回值 即请求还来的参数
        # 表示如果get200走不通,说明请求失败,就不需要继续
        rv = self.get200(uri, method, **params)
        # 将获取的返回值变为json格式
        return json.loads(rv.data)

    def get_succ_json(self, uri, method='GET', **params):
        data = self.get_json(uri, method, **params)
        self.assertEqual(data['rc'], Code.succ.value)
        return data
