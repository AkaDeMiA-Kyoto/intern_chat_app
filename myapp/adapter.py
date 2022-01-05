from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        # 気を付けて！アカウント作成時にユーザー画像を登録していないのにuser.imageを更新しちゃうと、カスタムユーザーモデルでデフォルトで指定した画像が保存されなくなっちゃう～～～
        if form.cleaned_data.get('image') != None:
            user.image = form.cleaned_data.get('image')
        user.save()