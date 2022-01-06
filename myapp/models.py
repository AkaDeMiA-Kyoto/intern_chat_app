from django.db import models, connection
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUserManager(models.Manager):
    def raw_as_qs(self, raw_query, params=()):
        """Execute a raw query and return a QuerySet.  The first column in the
        result set must be the id field for the model.
        :type raw_query: str | unicode
        :type params: tuple[T] | dict[str | unicode, T]
        :rtype: django.db.models.query.QuerySet
        """
        cursor = connection.cursor()
        try:
            cursor.execute(raw_query, params)
            return self.filter(id__in=(x[0] for x in cursor))
        finally:
            cursor.close()

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    image = models.ImageField(upload_to='userimg/', default='userimg/defaultuser.png')
    regtime = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = 'CustomUser'

class Message(models.Model):
    # ForeignKeyを2種類作成するために、related_nameを別々で指定しておく
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver")
    sendtime = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.sendtime} | {self.sender} ->{self.receiver} | {self.content}"
