
from rest_framework import serializers
from app01 import models


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'

