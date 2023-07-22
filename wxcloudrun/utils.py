import hashlib
import os
from flask import g, current_app
from wxcloudrun.dao import query_voucher_by_code, delete_voucher_by_code, insert_voucher, update_voucher_status, query_all_voucher
from wxcloudrun.enums import VoucherStatus, Command, AdminCommand
from config import SEPARATOR, CODE_LINK_SEPARATOR

ADMIN_USER = []
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "#password#")
app = current_app


def process_content(content):
    commands = content.split("\n")

    if len(commands) == 0:
        return "无法识别的命令。\n"

    if commands[0] == Command.ADMIN_REGISTER:
        return process_admin_register(commands[1:])
    else:
        return process_user_fetch_voucher_link(commands[0])


def process_user_fetch_voucher_link(command):
    # TODO: input validation

    voucher_code = command
    voucher = query_voucher_by_code(voucher_code)
    if voucher is None:
        return "无效的兑换码。\n"

    if voucher.voucher_status == VoucherStatus.USED:
        return "兑换码已被使用。\n"

    voucher_link = voucher.voucher_link
    update_voucher_status(voucher_code, VoucherStatus.USED)
    return f"兑换链接：{voucher_link}\n"


def process_admin_register(command):
    if len(command) != 1:
        return "注册命令格式错误。"

    if command[0] != ADMIN_PASSWORD:
        return "注册密码错误。"

    user_name = g.data["FromUserName"]
    if user_name in ADMIN_USER:
        app.logger.info(f"Admin user {user_name} already registered.")
        return "已注册。"
    else:
        ADMIN_USER.append(user_name)
        app.logger.info(f"Successfully registered admin user: {user_name}")
        return "注册成功。"


def check_admin(user):
    return user in ADMIN_USER


def process_admin_content(content):
    commands = content.split("\n")
    if len(commands) == 0:
        return "无法识别的命令。\n"

    if commands[0] == AdminCommand.ADMIN_ADD_VOUCHER:
        return process_admin_add_voucher(commands[1:])
    elif commands[0] == AdminCommand.ADMIN_DELETE_VOUCHER:
        return process_admin_delete_voucher(commands[1:])
    elif commands[0] == AdminCommand.ADMIN_QUERY_VOUCHER:
        return process_admin_query_voucher(commands[1:])
    elif commands[0] == AdminCommand.ADMIN_QUERY_ALL_VOUCHER:
        return process_admin_query_all_voucher(commands[1:])
    elif commands[0] == Command.ADMIN_REGISTER:
        return process_admin_register(commands[1:])
    else:
        return "无法识别的命令。\n"


def process_admin_add_voucher(commands):
    # TODO: input validation

    messages = []

    for command in commands:
        voucher_code, voucher_link = command.split(CODE_LINK_SEPARATOR)
        # voucher_code = generate_voucher_code_by_voucher_link(voucher_link)
        voucher = query_voucher_by_code(voucher_code)
        if voucher is not None:
            message = f"{voucher.voucher_code}{SEPARATOR}{voucher.voucher_link}{SEPARATOR}链接已存在{SEPARATOR}{voucher.voucher_status}"
            messages.append(message)
            continue

        voucher = insert_voucher(voucher_code, voucher_link)
        if voucher is None:
            message = f"{voucher_code}{SEPARATOR}{voucher_link}{SEPARATOR}添加失败"
            messages.append(message)
            continue

        message = f"{voucher.voucher_code}{SEPARATOR}{voucher.voucher_link}{SEPARATOR}添加成功"
        messages.append(message)

    return "\n".join(messages)


def process_admin_query_all_voucher(commands):
    # TODO: input validation

    messages = []
    vouchers = query_all_voucher()
    if vouchers is None or len(vouchers) == 0:
        return "没有储存链接。\n"

    for voucher in vouchers:
        message = f"{voucher.voucher_code}{SEPARATOR}{voucher.voucher_link}{SEPARATOR}{voucher.voucher_status}"
        messages.append(message)

    return "\n".join(messages)


def process_admin_query_voucher(commands):
    # TODO: input validation

    messages = []
    for voucher_code in commands:
        voucher = query_voucher_by_code(voucher_code)
        if voucher is None:
            message = f"{voucher_code}{SEPARATOR}兑换码不存在"
            messages.append(message)
            continue

        message = f"{voucher.voucher_code}{SEPARATOR}{voucher.voucher_link}{SEPARATOR}{voucher.voucher_status}"
        messages.append(message)

    return "\n".join(messages)


def process_admin_delete_voucher(commands):
    # TODO: input validation

    messages = []
    for voucher_code in commands:
        voucher = query_voucher_by_code(voucher_code)
        if voucher is None:
            return "兑换码不存在。\n"

        delete_voucher_by_code(voucher_code)
        message = f"{voucher.voucher_code}{SEPARATOR}删除成功"
        messages.append(message)

    return "\n".join(messages)


def generate_voucher_code_by_voucher_link(voucher_link):
    # hash the voucher_link
    hash_object = hashlib.sha256(voucher_link.encode())
    hex_dig = hash_object.hexdigest()
    # take the first 8 alphanumeric characters of the hash
    code = hex_dig[:8]

    # ensure code is uppercase
    code = code.upper()

    # return the voucher code
    return code
