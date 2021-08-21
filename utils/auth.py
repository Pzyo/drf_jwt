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

