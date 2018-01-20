import os


class DefaultConfig(object):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rock1204@localhost/tigereye'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LOG_DIR = os.path.join(BASE_DIR, 'logs')
