from flask_sqlalchemy import SQLAlchemy
import pymysql
import config
import json
from datetime import datetime
from flask import Flask, request, Response, g


# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/ydxc'.format(config.username, config.password,
                                                                       config.db_address)

db = SQLAlchemy(app)


class VoucherStatus:
    UNUSED = '未核销'
    USED = '已核销'


class Voucher(db.Model):
    __tablename__ = 'Voucher'
    id = db.Column(db.Integer, primary_key=True)
    voucher_link = db.Column(db.String(1024), nullable=False)
    voucher_code = db.Column(
        db.String(1024, collation='utf8_bin'), nullable=False)
    voucher_status = db.Column(
        db.String(1024), nullable=False, default=VoucherStatus.UNUSED)
    created_at = db.Column('createdAt', db.TIMESTAMP,
                           nullable=False, default=datetime.now())


# db.drop_all()
db.create_all()


app.config.from_object('config')


@app.route('/api/send_message', methods=['POST'])
def send_message():
    from wxcloudrun.utils import check_admin, process_admin_content, process_content
    try:
        data = request.get_json()

        if data is None:
            raise Exception("Request body is empty")

        g.data = data
        user = data["FromUserName"]
        content = data["Content"]

        is_admin = check_admin(user)
        if is_admin:
            message = process_admin_content(content)

            res_body = {
                "ToUserName": data["FromUserName"],
                "FromUserName": data["ToUserName"],
                "CreateTime": int(datetime.now().timestamp()),
                "MsgType": "text",
                "Content": message
            }

            res_data = json.dumps(res_body, ensure_ascii=False)
            return Response(res_data, mimetype='application/json')

        else:
            message = process_content(content)

            res_body = {
                "ToUserName": data["FromUserName"],
                "FromUserName": data["ToUserName"],
                "CreateTime": int(datetime.now().timestamp()),
                "MsgType": "text",
                "Content": message
            }

            res_data = json.dumps(res_body, ensure_ascii=False)
            return Response(res_data, mimetype='application/json')

    except Exception as e:
        app.logger.error(f"Failed to parse request body: {e}")
        return Response(status=200)
