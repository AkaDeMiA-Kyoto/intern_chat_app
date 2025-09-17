from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

# Create your tests here.

class LoginTestCase(TestCase):
    def setUp(self):
        self.test_user=get_user_model().objects.create_user(
            username='test',
            email='test@test.com',
            password='testpassword###'
        )
        self.another_user=get_user_model().objects.create_user(
            username='another_user',
            email='another@another.com',
            password='1q2w7u8i'
        )

    def test_nologin_access(self):
        response=self.client.get(reverse_lazy('talk_room',kwargs={'user_id':self.another_user.id}))
        self.assertRedirects(
            response,
            reverse_lazy('login')+f'?next=/talk_room/{self.another_user.id}/'
        )
    
    def test_login_access(self):
        self.client.force_login(self.test_user)
        response=self.client.get(reverse_lazy('talk_room',kwargs={'user_id':self.another_user.id}))
        self.assertEqual(response.status_code,200)

    def test_chat(self):
        self.client.force_login(self.test_user)
        params={
            'talk':'test'
        }
        response=self.client.post(
            reverse_lazy('talk_room',kwargs={'user_id':self.another_user.id}),
            params
        )
        self.assertRedirects(
            response,
            reverse_lazy('talk_room',kwargs={'user_id':self.another_user.id})
        )