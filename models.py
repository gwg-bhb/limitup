#encoding: utf-8

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class DailyResult(db.Model):
    __tablename__ = 'daily_result_detail'
    date = db.Column(db.String, primary_key=True, nullable=False)
    code = db.Column(db.String, primary_key=True, nullable=False)
    ten_is_raiselimit = db.Column(db.String)
    ten_is_one = db.Column(db.String)
    close_is_raiselimit = db.Column(db.String)
    close_is_one = db.Column(db.String)
    time_raiselimit = db.Column(db.String, nullable=False)
    num_raiselimit = db.Column(db.Integer)

