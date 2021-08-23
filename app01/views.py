
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from app01 import models
from app01.ser import ArticleModelSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ArticleModelViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = ArticleModelSerializer
    authentication_classes = [JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated,]