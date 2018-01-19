from sqlalchemy import text
from tigereye.models import db, Model
from sqlalchemy.sql import func


class Play(db.Model, Model):
    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    mid = db.Column(db.Integer)

    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=0, nullable=False)

    price_type = db.Column(db.Integer)
    price = db.Column(db.Integer)
    market_price = db.Column(db.Integer)
    lowest_price = db.Column(db.Integer)

    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Integer, nullable=False, default=0, index=True)












