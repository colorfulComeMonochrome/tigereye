from tigereye.configs.default import DefaultConfig


# 测试状态下使用的配置
# 继承默认配置类
class TestConfig(DefaultConfig):
    TESTING = True
    JSON_SORT_KEYS = False
    # 显示sql语句
    SQLALCHEMY_ECHO = False
    # 使用sqlite数据库,不添加地址表示在内存中运行,关机后数据删除
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
