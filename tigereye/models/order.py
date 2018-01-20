from enum import unique, Enum
from random import randint

from tigereye.models import db, Model
from sqlalchemy import text
from sqlalchemy.sql import func
from tigereye.helper import tetime

"""
订单
   id
   影院id
   影厅id
   电影id
   排期id
   排期id
   取票码
   票数
   金额
   支付时间
   取票时间
   退款时间
   创建时间
   最后更新时间
   状态
"""


@unique
class OrderStatus(Enum):
    """已锁座"""
    locked = 1
    """解锁"""
    unlocked = 2
    """自动解锁(超过一定时间未操作被系统自动解锁)"""
    auto_unlocked = 3
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """退款"""
    refund = 6


class Order(db.Model, Model):
    __tablename__ = 'orders'
    # 订单ID,自己的订单号
    oid = db.Column(db.String(32), primary_key=True)
    # 销售方订单号
    sell_order_num = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    sid = db.Column(db.String(32))
    # 取票码
    ticket_flag = db.Column(db.String(64))
    tickets_num = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    paid_time = db.Column(db.DateTime)
    printed_time = db.Column(db.DateTime)
    refund_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Integer, nullable=False, default=0, index=True)

    # 类方法,创建订单
    @classmethod
    def create(cls, cid, pid, sid):
        order = cls()
        # 订单号:时间+6位随机数+pid
        order.oid = '%s%s%s' % (tetime.now(), randint(100000, 999999), pid)
        order.cid = cid
        order.pid = pid
        # 如果座位是多选,则传入的参数为列表,将其转化为以“,”号分割的字符串
        # 该字符串会在multi_int装饰器中被处理成参数列表
        if type(sid) == list:
            order.sid = ','.join(str(i) for i in sid)
        else:
            order.sid = sid
        return order

    # 通过订单号查找订单
    @classmethod
    def getby_order_num(cls, order_num):
        return Order.query.filter_by(sell_order_num=order_num).first()

    def gen_ticket_flag(self):
        self.ticket_flag = ''.join([str(randint(1000, 9999)) for i in range(8)])

    # 简化后的写法，实际中需要进行加密
    def validate(self, ticket_flag):
        return self.ticket_flag == ticket_flag

    @classmethod
    def getby_ticket_flag(cls, ticket_flag):
        return cls.query.filter_by(ticket_flag=ticket_flag).first()
