from sqlalchemy.exc import OperationalError
from wxcloudrun import db, Voucher
from flask import current_app

logger = current_app.logger


def query_voucher_by_code(code):
    try:
        voucher = Voucher.query.filter(Voucher.voucher_code == code).first()
        logger.info("query_voucher_by_code voucher_code= {} ".format(code))
        return voucher
    except OperationalError as e:
        logger.info("query_voucher_by_code errorMsg= {} ".format(e))
        return None


def delete_voucher_by_code(code):
    try:
        voucher = query_voucher_by_code(code)
        if voucher is None:
            return
        db.session.delete(voucher)
        db.session.commit()
        logger.info("delete_voucher_by_code voucher_code= {} ".format(code))
    except OperationalError as e:
        logger.info("delete_voucher_by_code errorMsg= {} ".format(e))


def insert_voucher(voucher_code, voucher_link):
    try:
        voucher = Voucher(voucher_code=voucher_code, voucher_link=voucher_link)
        db.session.add(voucher)
        db.session.commit()
        logger.info("insert_voucher voucher= {} vocuher_link= {}".format(
            voucher_code, voucher_link))
        return voucher
    except OperationalError as e:
        logger.info("insert_voucher errorMsg= {} ".format(e))


def update_voucher_status(code, status):
    try:
        voucher = query_voucher_by_code(code)
        if voucher is None:
            return
        voucher.voucher_status = status
        db.session.flush()
        db.session.commit()
        logger.info(
            "update_voucher_status voucher_code= {} status= {}".format(code, status))
    except OperationalError as e:
        logger.info("update_voucher_status errorMsg= {} ".format(e))


def query_all_voucher():
    try:
        vouchers = Voucher.query.all()
        # logger.info("query_all_voucher vouchers= {} ".format(vouchers))
        return vouchers
    except OperationalError as e:
        logger.info("query_all_voucher errorMsg= {} ".format(e))
        return None
