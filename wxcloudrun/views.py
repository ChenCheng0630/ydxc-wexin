import json
from datetime import datetime
from flask import render_template, request, Response, jsonify, g, current_app
from wxcloudrun.dao import query_voucher_by_code, delete_voucher_by_code, insert_voucher, update_voucher_status
from wxcloudrun.model import Voucher
from wxcloudrun.utils import generate_voucher_code_by_voucher_link, check_admin, process_admin_content, process_content
from wxcloudrun import app


@app.route('/api/send_message', methods=['POST'])
def send_message():

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
        return Response(status=400)
