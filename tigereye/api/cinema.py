from flask_classy import FlaskView
from flask import jsonify, request
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.extensions.validator import Validator

class CinemaView(ApiView):
    def all(self):
        cinemas = Cinema.query.all()
        return cinemas

    def get(self):
        cid = request.args['cid']
        # cid = request.args['']

        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        return cinema

    @Validator(cid=int)
    def halls(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            # 1表示约定好的错误码
            return Code.cinema_does_not_exist, request.args
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema

