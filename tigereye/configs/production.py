from tigereye.configs.default import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False
    JSON_SORT_KEYS = False
    JASON_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_ECHO = False

    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'test1@iguye.com'
    EMAIL_HOST_PASSWORD = 'P67844QUssW3'
    EMAIL_USE_SSL = True
    ADMINS = ['768186932@qq.com', '13664069165@163.com']
