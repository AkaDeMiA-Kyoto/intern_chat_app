from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress
from django.dispatch import receiver

@receiver(email_confirmed)  # 確認メールによって確認された場合に実行される
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email) # 新たに確認されたメール以外はすべて古いメールとする
    if old_email.exists():
        user.email = email_address.email
        user.save()
        email_address.primary = True # メインのメールアドレスにする
        email_address.save()
        old_email.delete()