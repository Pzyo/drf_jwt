
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