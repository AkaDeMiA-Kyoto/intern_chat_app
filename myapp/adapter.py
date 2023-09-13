# member/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from .models import *
from django.shortcuts import resolve_url

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        print("********** WOW ****************")
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        user.image = form.cleaned_data.get('image')
        return super(AccountAdapter, self).save_user(request, user, form, commit)