from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11)
    icon = models.ImageField(upload_to='icon')  # ImageField依赖于pillow模块
