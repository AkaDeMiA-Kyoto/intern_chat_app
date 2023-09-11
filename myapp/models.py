from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", default="images/noimage.png"
    )