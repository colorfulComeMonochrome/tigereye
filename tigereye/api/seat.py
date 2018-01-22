from datetime import datetime

from flask import request
from flask_classy import route
from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, multi_complex_int
from tigereye.helper.code import Code
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat, SeatType


class SeatView(ApiView):
    # 选座的api   将所选座位的电影id(pid), 座位id(sid(可以多选), 价格(price), order_num(销售方订单号))
    @Validator(pid=int, sid=multi_int, price=int, order_num=str)
    @route('/lock/', methods=['POST'])
    def lock(self):
        # 从装饰器的try中定义的request.params中取出查找具体座位的参数
        pid = request.params['pid']
        sid = request.params['sid']
        price = request.params['price']
        order_num = request.params['order_num']
        # 通过pid找到具体的排期
        play = Play.get(pid)
        # 如果从数据库中找不到对应的排期(play为空)
        if not play:
            # 返回排期不存在的状态码和请求的参数
            return Code.play_does_not_exist, request.params
        # 如果参数中的票价低于最低票价，返回票价过低状态码和参数
        if price < play.lowest_price:
            return Code.prcice_less_than_the_lowest_price, request.params
        # 调用排期座位(PlaySeat)中的类函数lock
        # 锁定已选的排期座位,locked_seats_num是lock函数的返回值,代表锁定的座位数目，lock()中对应参数是rows
        locked_seats_num = PlaySeat.lock(order_num, pid, sid)
        # 如果返回的locked_seats_numrows(rows)值为0 则表示锁定座位失败
        if not locked_seats_num:
            return Code.seat_lock_failed, {}
        # 如果locked_seats_num(reows)值不为0
        # 创建订单
        order = Order.create(play.cid, pid, sid)
        order.sell_order_num = order_num
        order.status = OrderStatus.locked.value
        order.tickets_num = locked_seats_num
        # 保存订单
        order.save()
        # 返回锁定的座位数
        return {'locked_seats_num': locked_seats_num}

    @Validator(pid=int, sid=multi_int, order_num=str)
    @route('/unlock/', methods=['POST'])
    def unlock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        order_num = request.params['order_num']
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, request.params

        order = Order.getby_order_num(order_num)
        if not order:
            return Code.order_does_not_exist, request.params

        unlocked_seats_num = PlaySeat.unlock(order_num, pid, sid)
        if not unlocked_seats_num:
            return Code.seat_unlock_failed, {}
        order.status = OrderStatus.unlocked.value
        order.save()
        return {'unlock_seats_num': unlocked_seats_num}

    # seats:1,200,5000|2,200,5000
    @Validator(seats=multi_complex_int, order_num=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        order_num = request.params['order_num']
        order = Order.getby_order_num(order_num)
        if not order:
            return Code.order_does_not_exist, request.params
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {
                'order_num': order_num,
                'status': order.status,
            }
        order.sell_order_num = request.params['order_num']
        # 订单的金额,如果金额不存在则等于0
        # a = a or b 用法:    a = a, 如果a为空,则a = b
        order.amount = order.amount or 0
        sid_list = []
        for sid, handle_fee, price in seats:
            sid_list.append(sid)
            order.amount += handle_fee + price
        bought_seats_num = PlaySeat.buy(order_num, order.pid, sid_list)
        if not bought_seats_num:
            return Code.seat_buy_failed, {}
        order.tickets_num = len(seats)
        order.paid_time = datetime.now()
        order.status = OrderStatus.paid.value
        # order的内部函数,生成一个由32位随机数组成的取票码(真是情况下,表中应该增加unique字段)
        order.gen_ticket_flag()
        order.save()
        return {
            'bought_seats_num': bought_seats_num,
            'ticket_flag': order.ticket_flag
        }
