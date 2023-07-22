class VoucherStatus:
    UNUSED = '未核销'
    USED = '已核销'


class Command():
    ADMIN_REGISTER = "/注册"


class AdminCommand():
    ADMIN_ADD_VOUCHER = "/添加"
    ADMIN_DELETE_VOUCHER = "/删除"
    ADMIN_QUERY_VOUCHER = "/查询"
    ADMIN_QUERY_ALL_VOUCHER = "/查询所有"
    ADMIN_LOGOUT = "/退出登录"
