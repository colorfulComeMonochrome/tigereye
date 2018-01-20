from .helper import FlaskTestCase
from flask import json
from tigereye.helper.code import Code


class TestApiCinema(FlaskTestCase):
    def test_cinema_all(self):
        # response = self.app.get('/cinema/all/')
        # self.assertEquals(response.status_code, 200)
        # data = json.loads(response.data)
        # print(data)
        # self.assertEquals(data['rc'], Code.succ.value)
        self.get_succ_json('/cinema/all/')

    def test_cinema_halls(self):
        self.assert_get('/cinema/halls/', 400)
        data = self.get_succ_json('/cinema/halls/', cid=1)
        self.assertIsNotNone(data['data'])

    def test_cinema_get(self):
        # self.assert_get('/cinema/get/', 200)
        data = self.get_succ_json('/cinema/', cid=1)
        self.assertIsNotNone(data['data'])
