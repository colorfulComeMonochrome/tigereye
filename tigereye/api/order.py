from datetime import datetime

from flask import request
from flask_classy import route
from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, multi_complex_int
from tigereye.helper.code import Code
from tigereye.models.movie import Movie
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat, SeatType


class OrderView(ApiView):
    @route('/refund/', methods=['POST'])
    @Validator(order_num=str, ticket_flag=str, sid=multi_int)
    def refund_ticket(self):
        order_num = request.params['order_num']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']
        # 查找订单
        order = Order.getby_order_num(order_num)
        # 订单不存在
        if not order:
            return Code.order_does_not_exist, {'order_num': order_num}
        # 已取票
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        # 没付款
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        # 取票码失败
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        # 执行退款函数 refund_num是函数返回值，表示退款票数
        refund_num = PlaySeat.refund(order_num, order.pid, seats)
        # 票数为0时 表示退款失败
        if not refund_num:
            return Code.ticket_refund_failed, {}
        # 状态改为已退款
        order.status = OrderStatus.refund.value
        # 添加退款时间
        order.refund_time = datetime.now()
        order.save()
        return {'refund_num': refund_num}

    @route('/ticket/print/', methods=['POST'])
    @Validator(order_num=str, ticket_flag=str, sid=multi_int)
    def print_ticket(self):
        order_num = request.params['order_num']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']
        # 查找订单
        order = Order.getby_order_num(order_num)
        # 订单不存在
        if not order:
            return Code.order_does_not_exist, {'order_num': order_num}
        # 已取票
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        # 没付款
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        # 取票码错误
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        # 执行取票函数 printet_num是函数返回值，表示取票数
        printet_num = PlaySeat.print_tickets(order.sell_order_num, order.pid, seats)
        # 票数为0时 表示退款失败
        if not printet_num:
            return Code.ticket_print_failed, {}
        # 状态改为已退款
        order.status = OrderStatus.printed.value
        # 添加退款时间
        order.printed_time = datetime.now()
        order.save()
        return {'printed_num': printet_num}

    @route('/ticket/info/')
    @Validator(order_num=str)
    def ticket_info(self):
        order_num = request.params['order_num']
        # 查找订单
        order = Order.getby_order_num(order_num)
        # 订单不存在
        if not order:
            return Code.order_does_not_exist, {'order_num': order_num}
        order.play = Play.get(order.pid)
        order.movie = Movie.get(order.play.mid)
        order.tickets = PlaySeat.getby_order_num(order_num)
        return order
