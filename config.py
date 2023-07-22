import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", '')
db_address = os.environ.get("MYSQL_ADDRESS", 'localhost:3306')

# Messages
SEPARATOR = " | "
CODE_LINK_SEPARATOR = " "

# WebPage Image Path
MAIN_PAGE_IMAGE_PATH = os.environ.get(
    "MAIN_PAGE_IMAGE_PATH", "https://7072-prod-4gn24xra226391b7-1318704201.tcb.qcloud.la/qrcode_for_gh_c372ce103d00_1280.jpg?sign=824c97f6b02eeb4a60537436c40e52e6&t=1690018757")
