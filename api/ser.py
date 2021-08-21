
from rest_framework import serializers
from api.models import User
from rest_framework.exceptions import ValidationError

class UserModelSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=16, min_length=4, required=True, write_only=True)  # 因为re_password在表模型中没有, 需要在这定义

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 're_password', 'icon']
        extra_kwargs = {
            'username': {'max_length':16,'min_length':2},
            'password': {'write_only': True}
        }

    # 局部钩子
    def validate_phone(self, data):
        if not len(data) == 11:
            raise ValidationError('手机号不合法')
        return data

    # 全局钩子
    def validate(self, attrs):
        if not attrs.get('password') == attrs.get('re_password'):
            raise ValidationError('两次密码不一致')
        attrs.pop('re_password')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserReadonlyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'icon']

class UserImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['icon']


import re
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
class LoginModelSerializer(serializers.ModelSerializer):
    # username在数据中是唯一字段, post请求被认为是保存数据, 自己的校验就不通过(已存在用户)
    # 方式1, 重新覆盖username字段,
    username = serializers.CharField()
    # 方式2, 将username改为其他, 不与数据库对应

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        # 在这编写多方式登录的逻辑
        username = attrs.get('username')  # 用户名有三种方式
        password = attrs.get('password')

        # 用过判断, username数据不同, 查询字段不一样
        # 正则匹配
        if re.match('^1[3-9]\d{9}$', username):
            user = User.objects.filter(phone=username).first()
        elif re.match('^.+@.+$', username):
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if user: # 存在用户
            # 校验密码, 因为是密文, 要用check_password
            if user.check_password(password):
                # 签发token
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                self.context['token'] = token
                self.context['username'] = user.username
                return attrs
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')