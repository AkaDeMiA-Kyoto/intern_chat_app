from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress
from django.dispatch import receiver

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    print(f'メールアドレス「{email_address.email}」は確認されました')
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email)
    if old_email.exists():
        user.email = email_address.email
        user.save()
        email_address.primary = True # メインのメールアドレスにする
        email_address.save()
        old_email.delete()