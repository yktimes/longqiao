import datetime
import re

from rest_framework_jwt.settings import api_settings
from django.contrib.auth.backends import ModelBackend

from .models import User

# def get_user_by_account(account):
#     """
#     根据帐号获取user对象
#     :param account: 账号，可以是用户名，也可以是手机号
#     :return: User对象 或者 None
#     """
#     try:
#         if re.match('^1[3-9]\d{9}$', account):
#             # 帐号为　学号
#             user = User.objects.get(StudentID=account)
#         else:
#             # 帐号为用户名
#             user = User.objects.get(username=account)
#     except User.DoesNotExist:
#         return None
#     else:
#         return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义学号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.get(StudentID=username)

        if user is not None and user.check_password(password):
            return user


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.StudentID,
        'username': user.username
    }

# 生成　token
def make_token(user):
    """
    生成　token
    :param user: user对象
    :return: 增加了token的user对象
    """
    # 补充生成记录登录状态的token
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = token



    print('user',user)
    return user



def howLongDays(date):

    """
    计算时间间隔
    :param date: 时间格式化日期　"20160903"　2019年9月3日
    :return:
    """

    d1 = datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d'),'%Y-%m-%d')

    d2 = datetime.datetime.strptime(date, '%Y%m%d')


    delta = d1 - d2

    return delta.days