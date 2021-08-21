import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework import exceptions
from django.utils.translation import ugettext as _


class MyToken(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get('HTTP_AUTHORIZATION', b'')

        if jwt_value is None:
            return None

        # 认证
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Token失效')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('认证失败')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

def my_jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'msg': '登录成功',
        'status': 100,
        'username': user.username
    }

from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.utils import jwt_decode_handler
import jwt
from api import models

class MyJwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get('HTTP_AUTHORIZATION', b'')
        if jwt_value is None:
            # 没有值直接抛异常
            raise AuthenticationFailed('您没有携带认证信息')
        # jwt提供了通过三段token, 取出payload的方法, 并且有校验功能
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('签名过期')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('非法用户')
        except Exception as e:
            raise AuthenticationFailed(str(e))

        # 因为payload就是用户信息的字典
        # 需要得到user对象, 第一种, 去数据库查
        # user = models.User.objects.get(pk=payload.get('user_id'))
        # 第二种不查库
        user = models.User(id=payload.get('user_id'), username=payload.get('username'))
        return user, jwt_value

class MyJwtJsonAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get('HTTP_AUTHORIZATION', b'')
        if jwt_value is None:
            # 没有值直接抛异常
            raise AuthenticationFailed('您没有携带认证信息')
        # jwt提供了通过三段token, 取出payload的方法, 并且有校验功能
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('签名过期')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('非法用户')
        except Exception as e:
            raise AuthenticationFailed(str(e))

        user = self.authenticate_credentials(payload)

        return user, jwt_value

