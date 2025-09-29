from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import User

# Create your tests here.
User = get_user_model()
class NoLogonTest(TestCase):
    def setUp(self):
        self.mio = User.objects.create_user(username="mio", password="mio123", email="mio@example.com")

    def if_not_login(self):
        url = reverse('myapp:talk_room', kwargs={'username':self.mio.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        try:
            login_url = reverse('login')
        except Exception:
            login_url = settings.LOGIN_URL

        expected = f"{login_url}?next={url}"

        self.assertRedirects(response, expected, fetch_redirect_response=False)

class LoginTest(TestCase):
    def setUp(self):
        self.mio = User.objects.create_user(username="mio", password="mio123")
        self.imada = User.objects.create_user(username="imada", password="imada123")
    def login_user_access(self):
        self.client.login(username="mio", password="mio123")
        url = reverse("talk_room", kwargs={"username": self.imada.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["friend"], self.imada)