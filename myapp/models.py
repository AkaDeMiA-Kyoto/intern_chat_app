from django.db import models
from accounts.models import Profile

class Message(models.Model):
    sender=models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sender"
    )
    receiver=models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="receiver"
    )
    content=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = "Message"
