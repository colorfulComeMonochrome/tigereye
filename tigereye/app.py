from flask import Flask
from flask_classy import FlaskView
from tigereye.models import db, JSONEncoder


def create_app(debug=True):
    app = Flask(__name__)
    # app.debug = debug
    app.config.from_object('tigereye.configs.default.DefaultConfig')
    app.json_encoder = JSONEncoder
    configure_views(app)
    db.init_app(app)
    return app


def configure_views(app):
    from tigereye.api.cinema import CinemaView
    from tigereye.api.movie import MovieView
    from tigereye.api.misc import MiscView
    from tigereye.api.hall import HallView
    # locals()  获取局部命名空间中的所有局部变量(包括属性，对象，方法等等)
    for view in locals().values():
        # print(type(view))
        # print(view)
        # type的类型是type  HallView的类型是type
        if type(view) == type and issubclass(view, FlaskView):

            view.register(app)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
