from django.urls import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory, TransactionTestCase
from django.contrib.auth.models import AnonymousUser
from .forms import *
from .models import *
from .views import *

# 書き途中

class FormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_when_given_proper_data(self):
        params = {
            'username': 'testusername',
            'email': 'example@example.com',
            'password1': 'passwordexample',
            'password2': 'passwordexample',
        }
        form = CustomSignupForm(params)
        self.assertTrue(form.is_valid())

    def test_invalid_when_given_wrong_passwords(self):
        params = {
            'username': 'testusername',
            'email': 'example@example.com',
            'password1': 'passwordexample',
            'password2': 'passw0rdexample',
        }
        form = CustomSignupForm(params)
        self.assertFalse(form.is_valid())

    def test_invalid_when_given_wrong_email(self):
        params = {
            'username': 'testusername',
            'email': 'exampleaexample.com',
            'password1': 'passwordexample',
            'password2': 'passw0rdexample',
        }
        form = CustomSignupForm(params)
        self.assertFalse(form.is_valid())

    def test_invalid_when_given_existing_email(self):
        CustomUser.objects.create(username='testusername', email='example@example.com', password='passwordexample')

        params = {
            'username': 'testusername2',
            'email': 'example@example.com',
            'password1': 'passwordexample',
            'password2': 'passwordexample',
        }
        form = CustomSignupForm(params)
        self.assertFalse(form.is_valid())

class FriendsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create(username='testuser', email='testuser@example.com', password='passtestworduser')
        CustomUser.objects.create(username='testuser1', email='testuser1@example.com', password='passtestworduser')
        CustomUser.objects.create(username='testuser2', email='testuser2@example.com', password='passtestworduser')

    def test_get(self):
        request = self.factory.get('friends')
        request.user = self.user
        view = Friends.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_should_redirect_if_user_does_not_login(self):
        request = self.factory.get('friends')
        request.user = AnonymousUser()
        view = Friends.as_view()
        response = view(request)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_should_show_two_friends(self):
        friends_view = Friends()
        request = self.factory.get('friends')
        request.user = self.user
        friends_view.request = request
        context = friends_view.get_context_data()

        self.assertEqual(len(context['friends']), 2)

    def test_should_show_one_friend_with_filter(self):
        friends_view = Friends()
        request = self.factory.get('friends', {'filter': '1'})
        request.user = self.user
        friends_view.request = request
        context = friends_view.get_context_data()

        self.assertEqual(len(context['friends']), 1)
        self.assertEqual(context['friends'][0]['user'].username, 'testuser1')

class TalkRoomViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create(username='testuser', email='testuser@example.com', password='passtestworduser')
        self.user1 = CustomUser.objects.create(username='testuser1', email='testuser1@example.com', password='passtestworduser')
        self.user2 = CustomUser.objects.create(username='testuser2', email='testuser2@example.com', password='passtestworduser')

    def test_get(self):
        friend_id = self.user1.id
        request = self.factory.get(reverse('talk_room', kwargs={"id": friend_id}))
        request.user = self.user
        view = TalkRoom.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)