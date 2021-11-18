from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.shortcuts import redirect

from allauth.account.models import EmailAddress

# メールアドレス変更の際はデータベースから古いメールアドレスを削除する
@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    customuser = request.user
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email)
    if old_email.exists():
        customuser.email = email_address.email
        user.email = email_address.email
        user.save()
        email_address.primary = True
        email_address.save()
        old_email.delete()
    else:
        pass