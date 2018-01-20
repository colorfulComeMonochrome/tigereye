from flask_classy import FlaskView
from flask import jsonify
from tigereye.models.movie import Movie
from tigereye.api import ApiView
from tigereye.helper.code import Code


class MovieView(ApiView):
    def all(self):
        return Movie.query.all()
