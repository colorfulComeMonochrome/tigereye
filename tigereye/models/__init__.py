from flask_sqlalchemy import SQLAlchemy
from flask import json as _json

# 创建SQLAlchemy的实例化对象,连接数据库,数据库的配置信息在config中
db = SQLAlchemy()

# 自己定义的mdel类,使用时需要同时继承此类和sqlalchemy类,
# 不能自己写一个类来继承是因为sqlalchemy类的子类
class Model(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    def put(self):
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()

    def delete(self):
        db.session.delete(self)

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    # 将数据json化
    def __json__(self):
        # vars(self):获取类内部的属性(字典形式)
        # vars(self).keys():  获取类内部属性的键
        keys = vars(self).keys()
        print(vars(self))
        print(keys)
        data = {}
        for key in keys:
            # 如果该属性不是内部属性
            if not key.startswith('_'):
                data[key] = getattr(self, key)
        return data


# 改写json.JSONEncoder类
# 该配置在创建app时生效
class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        # 如果传入的参数类型是我们自己定义的类,则运行自己类里的json化函数
        if isinstance(o, db.Model):
            return o.__json__()
        return _json.JSONEncoder.default(self, o)
