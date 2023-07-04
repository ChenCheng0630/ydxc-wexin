from datetime import datetime
from flask import current_app


class VoucherStatus:
    UNUSED = '未核销'
    USED = '已核销'


class Voucher(db.Model):
    __tablename__ = 'Voucher'
    id = db.Column(db.Integer, primary_key=True)
    voucher_link = db.Column(db.String(1024), nullable=False)
    voucher_code = db.Column(db.String(1024), nullable=False)
    voucher_status = db.Column(
        db.String(1024), nullable=False, default=VoucherStatus.UNUSED)
    created_at = db.Column('createdAt', db.TIMESTAMP,
                           nullable=False, default=datetime.now())


db.create_all()
