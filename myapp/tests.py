from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class LoginViewTests(TestCase):
    def setUp(self):
        """ テストのための準備（ユーザーをデータベースに登録する） """
        self.test_user = get_user_model().objects.create_user(
            username='test_user',
            email='test@example.com',
            password='test_password'
        )
        self.another_user = get_user_model().objects.create_user(
            username='test2_user',
            email='test2@example.com',
            password='test2_password'
        )
    
    def test_normal_access_with_no_login(self):
        """ ログインしていない状態でアクセスする """
        response = self.client.get(
            reverse_lazy('talk_room', kwargs={'user_id': self.another_user.id})
        )
        # ログイン画面にリダイレクトされることを検証
        self.assertRedirects(
            response,
            reverse_lazy('login') + f'?next=/talk_room/{self.another_user.id}/'
        )

    def test_normal_access_with_login(self):
        """ ログインした状態でアクセスする """
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse_lazy('talk_room', kwargs={'user_id': self.another_user.id})
        )
        # ステータスコードが 200 になることを検証
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        """ メッセージを送信する """
        self.client.force_login(self.test_user)
        params = {
            'talk': 'テストメッセージ',
        }
        response = self.client.post(
            reverse_lazy('talk_room', kwargs={'user_id': self.another_user.id}),
            params
        )
        # 作成後に再びこのページにリダイレクトされることを検証
        self.assertRedirects(
            response,
            reverse_lazy('talk_room', kwargs={'user_id': self.another_user.id}),
        )