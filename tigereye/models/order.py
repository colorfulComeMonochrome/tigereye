from tigereye.models import db, Model
from sqlalchemy import text
from sqlalchemy.sql import func


class Order(db.Model, Model):
    __tablename__ = 'orders'
    # 订单ID,自己的订单号
    oid = db.Column(db.String(32), primary_key=True)
    # 销售方订单号
    sell_order_num = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
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





