
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^article/$', views.ArticleModelViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    url(r'^article/(?P<pk>\d+)$', views.ArticleModelViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]