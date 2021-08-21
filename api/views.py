
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.auth import MyToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_response_payload_handler

class BookView(APIView):
    authentication_classes = [JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    # authentication_classes = [MyToken,]

    def get(self, request):
        return Response('ok')


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from api.models import User
from api.ser import UserModelSerializer, UserReadonlyModelSerializer, UserImageModelSerializer

class RegisterView(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    # 假设get请求和post请求, 用的序列化类不一样
    # 需要重写get_serializer_class, 返回啥, 用的序列化类就是啥
    def get_serializer_class(self):
        # print(self.action)  # 目前只有两种情况:  create, retrieve
        if self.action == 'create':
            return UserModelSerializer
        elif self.action == 'retrieve':
            return UserReadonlyModelSerializer
        elif self.action == 'update':
            return UserImageModelSerializer


# 手动签发token, 支持多方式登录

from rest_framework.viewsets import ViewSetMixin, ViewSet
from api import ser

# class Login2View(ViewSetMixin,APIView):
class Login2View(ViewSet):
    # 这是登录接口
    def login(self, request, *args, **kwargs):
        # 1. 需要有一个序列化的类
        # 2. 生成序列化类对象
        login_ser = ser.LoginModelSerializer(data=request.data)
        # 3. 调用序列化类对象的is_vaildad
        login_ser.is_valid(raise_exception=True)
        token = login_ser.context.get('token')
        username = login_ser.context.get('username')
        # 4. return
        return Response({'status':100, 'msg':'登录成功', 'token':token, 'username':username})
