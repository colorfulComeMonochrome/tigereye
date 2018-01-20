from datetime import datetime

from tigereye.models import db, Model
from sqlalchemy import text
from enum import Enum, unique


@unique
class SeatStatus(Enum):
    """正常状态，可购买"""
    ok = 0
    """已锁定"""
    locked = 1
    """已售出"""
    sold = 2
    """已打票"""
    printed = 3
    """已预订"""
    booked = 9
    """维修中"""
    repair = 99


@unique
class SeatType(Enum):
    """过道"""
    road = 0
    """单人"""
    single = 1
    """双人"""
    couple = 2
    """保留座位"""
    reserve = 3
    """残疾专座"""
    for_disable = 4
    """VIP专座"""
    vip = 5
    """震动座椅"""
    shake = 6


"""
座位
   id
   影院id
   影厅id
   座位类型
   是否是情侣座
   坐标x
   坐标y
   排（A/第1排）
   列（某一列）
   区域
   状态

"""
"""
排期座位
   id
   订单号
   影院id
   影厅id
   座位类型
   是否是情侣座
   坐标x
   坐标y
   排（A/第1排）
   列（某一列）
   区域
   状态
   锁定时间
   创建时间
"""


class Seat(db.Model, Model):
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    row = db.Column(db.String(16))
    column = db.Column(db.String(16))

    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    love_seats = db.Column(db.String(16))
    status = db.Column(db.Integer, nullable=False, default=0, index=True)


class PlaySeat(db.Model, Model):
    psid = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)

    sid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(16))
    column = db.Column(db.String(16))
    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    love_seats = db.Column(db.String(16))
    status = db.Column(db.Integer, nullable=False, default=0, index=True)

    lock_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

    def copy(self, seat):
        self.sid = seat.sid
        self.cid = seat.cid
        self.hid = seat.hid
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.seat_type = seat.seat_type
        self.love_seats = seat.love_seats
        self.status = seat.status

    # 锁定已选的排期座位
    @classmethod
    def lock(cls, order_num, pid, sid_list):
        # 创建数据库会话,通过会话进行数据库交互
        session = db.create_scoped_session()
        # 先通过参数传入的pid,sid及订票的状态码查找排期座位
        rows = session.query(PlaySeat).filter(
            PlaySeat.pid == pid,
            PlaySeat.status == SeatStatus.ok.value,
            PlaySeat.sid.in_(sid_list)
            # 修改排期座位中的属性:　销售方订单号(order_num),状态码,锁定时间
        ).update({
            'order_num': order_num,
            'status': SeatStatus.locked.value,
            'lock_time': datetime.now()
            # synchronize_session: 表示在修改数据库是不阻塞其他修改请求
        }, synchronize_session=False)
        # update操作后数据库会返回一个返回值,表示修改了几条PlaySeat数据
        # 如果修改的数据数目为0,表示修改失败
        if rows != len(sid_list):
            session.rollback()
            return 0

        session.commit()
        # 返回修改的数据条数/即锁定座位数
        return rows

    # 解锁排期座位
    @classmethod
    def unlock(cls, order_num, pid, sid_list):
        # 创建链接数据库的事务
        session = db.create_scoped_session()
        # rows 是提交到数据库中之后数据库返回的返回值
        # 通过订单号,状态码来查找对应座位,并将销售方订单号修改为空,状态码改为可售
        rows = session.query(PlaySeat).filter_by(
            order_num=order_num,
            status=SeatStatus.locked.value).update({
            'order_num': None,
            'status': SeatStatus.ok.value,
        }, synchronize_session=False)
        # 同理，如果返回值为0,表示修改了0条数据,修改失败
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        # 返回修改的数据条数/即解锁座位数
        return rows

    # 付款
    @classmethod
    def buy(cls, order_num, pid, sid_list):
        session = db.create_scoped_session()
        # 数据库会话返回值
        rows = session.query(PlaySeat).filter_by(
            # 通过订单号和取票码查找
            order_num=order_num,
            status=SeatStatus.locked.value,
        ).update({
            'status': SeatStatus.sold.value,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def refund(cls, order_num, pid, sid_list):
        session = db.create_scoped_session()
        # 数据库会话返回值
        rows = session.query(PlaySeat).filter_by(
            # 通过订单号和取票码查找
            order_num=order_num,
            status=SeatStatus.sold.value,
        ).update({
            'status': SeatStatus.ok.value,
            'order_num': None,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def print_tickets(cls, order_num, pid, sid_list):
        session = db.create_scoped_session()
        # 数据库会话返回值
        rows = session.query(PlaySeat).filter_by(
            # 通过订单号和取票码查找
            order_num=order_num,
            status=SeatStatus.sold.value,
        ).update({
            'status': SeatStatus.printed.value,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def getby_order_num(cls, order_num):
        return cls.query.filter_by(order_num=order_num).all()
