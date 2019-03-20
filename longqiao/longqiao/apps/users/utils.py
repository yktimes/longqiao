import datetime


from rest_framework_jwt.settings import api_settings


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