import os
import logging
from logging import FileHandler, Formatter
from logging.handlers import SMTPHandler

from flask import Flask
from flask_classy import FlaskView
from tigereye.models import db, JSONEncoder


# 创建app的方法
def create_app(config=None):
    app = Flask(__name__)
    # app.debug = debug
    app.config.from_object('tigereye.configs.default.DefaultConfig')
    app.config.from_object(config)
    # 应用自己定义的jsonencoder类
    app.json_encoder = JSONEncoder

    if not app.debug:
        app.logger.setLevel(logging.INFO)

        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            app.config['ADMINS'],
            'TIGEREYE ALERT',
            credentials=(app.config['EMAIL_HOST_USER'],
                         app.config['EMAIL_HOST_PASSWORD'])
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter("""
        Message Type: %(levelname)s
        Location:     %(pathname)s: %(lineno)d
        Module:       %(module)s
        Function:     %(funcName)s
        Time:         %(asctime)s
        
        Message:
        
        %(message)s
        """))
        app.logger.addHandler(mail_handler)
        print(app.config['EMAIL_HOST'],
              app.config['EMAIL_PORT'],
              app.config['ADMINS'],
              app.config['EMAIL_HOST_USER'],
              app.config['EMAIL_HOST_PASSWORD'])
        file_handler = FileHandler(os.path.join(app.config['LOG_DIR'], 'app.log'))
        file_handler.setLevel(logging.INFO)
        # 关键字占位符 可以传字典
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s : %(message)s'
        ))
        app.logger.addHandler(file_handler)

    configure_views(app)
    db.init_app(app)
    app.logger.info('app created completed')
    return app


# 配置app内默认导入的包，方便shell脚本测试
def configure_views(app):
    from tigereye.api.cinema import CinemaView
    from tigereye.api.movie import MovieView
    from tigereye.api.misc import MiscView
    from tigereye.api.hall import HallView
    from tigereye.api.play import PlayView
    from tigereye.api.seat import SeatView
    from tigereye.api.order import OrderView
    from tigereye.models.seat import PlaySeat
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
