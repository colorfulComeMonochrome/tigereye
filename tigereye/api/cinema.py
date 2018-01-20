from flask_classy import FlaskView
from flask import jsonify, request

from tigereye import app
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.models.movie import Movie
from tigereye.models.play import Play
from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.extensions.validator import Validator


class CinemaView(ApiView):
    def all(self):
        # 获取所有电影院的信息
        cinemas = Cinema.query.all()
        return cinemas

    # get路由是特殊指定的,需要访问/cinema/?cid=1  直接访问
    # 把@Validator放到get()函数定义处,相当于执行了语句get = Validator(get)
    @Validator(cid=int)
    def get(self):
        # print(type(request))
        print(request.params)
        print(request.args)
        print(type(request.args))
        cid = request.params['cid']
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

    @Validator(cid=int)
    def plays(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        cinema.plays = Play.query.filter_by(cid=cid).all()
        for play in cinema.plays:
            play.movie = Movie.get(play.mid)
        return cinema
