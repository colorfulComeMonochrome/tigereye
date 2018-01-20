from flask import request

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator
from tigereye.models.seat import PlaySeat, SeatType


class PlayView(ApiView):
    # 返回所有选中排期的可选座位信息
    @Validator(pid=int)
    def seats(self):
        # pid = request.params['pid']
        return PlaySeat.query.filter(
            PlaySeat.pid == request.params['pid'],
            # seat_type=1表示座位已被锁定
            PlaySeat.seat_type != SeatType.road.value
        ).all()
