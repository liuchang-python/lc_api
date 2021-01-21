from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


def get_user_by_account(account):
    try:
        # 三者只要满足其中一个条件 则返回查询到用户
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user


class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        根据账号获取用户对象
        :param request: 请求对象
        :param username:  前端输入的登录账号：用户名 手机 邮箱
        :param password: 用户明文密码
        :return: 查询出的用户
        """
        # 根据条件查询用户
        user = get_user_by_account(username)

        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None
