from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from allauth.account.models import EmailAddress

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    customuser = request.user
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email)
    if old_email.exists():
        customuser.email = email_address.email
        user.email = email_address.email
        user.save()
        customuser.save()
        email_address.primary = True
        email_address()
        old_email.delete()
    else:
        pass