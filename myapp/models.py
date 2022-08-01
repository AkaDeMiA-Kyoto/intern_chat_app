from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager, PermissionsMixin
    )
from django.urls import reverse_lazy
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
                    username=username,
                    email=email
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    icon = models.ImageField(default="default_profile_img.jpeg")
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('index')

class Talk(models.Model):
    message = models.CharField(max_length=35)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_talk"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_talk"
    )
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.sender, self.receiver)

