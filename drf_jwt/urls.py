"""drf_jwt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api import views
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken, obtain_jwt_token
# 基类: JSONWebTokenAPIView, 继承于APIView
# ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken都继承于JSONWebTokenAPIView
'''
源码中:
obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
'''

from rest_framework.routers import SimpleRouter
routers = SimpleRouter()
routers.register('register', views.RegisterView, basename='register')

from django.views.static import serve  # django内置的视图函数FBV
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/', ObtainJSONWebToken.as_view()),
    url(r'^login/', obtain_jwt_token),
    # 开放MEDIA文件夹
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^books/', views.BookView.as_view()),
    # url(r'^register/', views.RegisterView.as_view(actions={'post':'create'})),
    url('', include(routers.urls)),  # 方式2

    url(r'^login2/', views.Login2View.as_view(actions={'post':'login'})),
]

# urlpatterns += routers.urls # 方式1