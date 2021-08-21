
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.auth import MyToken
from rest_framework.permissions import IsAuthenticated

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
