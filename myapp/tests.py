from django.test import TestCase, Client
from .models import User
from django.urls import reverse_lazy


class LoginTests(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username="test",
            password="test",
            email="test@example.com",
        )
        self.another_user = User.objects.create_user(
            username="test_another",
            password="test",
            email="test@example.com",
        )

    def test_talk_without_auth(self):
        response = Client().get(
            reverse_lazy("talk_room", kwargs={"user_id": self.another_user.id}),
        )
        self.assertRedirects(
            response,
            reverse_lazy("login") + f"?next=/talk_room/{self.another_user.id}/",
        )

    def test_talk_with_auth(self):
        Client().force_login(self.test_user)
        responce = Client().get(
            reverse_lazy("talk_room", kwargs={"user_id": self.another_user.id})
        )

        self.assertEqual(responce.status_code, 302)

    def test_talk_send_mail(self):
        self.client.force_login(self.test_user)
        params = {
            "talk": "テストメッセージ",
        }
        response = self.client.post(
            reverse_lazy("talk_room", kwargs={"user_id": self.another_user.id}), params
        )
        # 作成後に再びこのページにリダイレクトされることを検証
        self.assertRedirects(
            response,
            reverse_lazy("talk_room", kwargs={"user_id": self.another_user.id}),
        )
