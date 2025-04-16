from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


class LoggedInTestCase(TestCase):

    def setUp(self):
        self.password = "testpassword123"
        self.test_user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password=self.password,
        )
        self.client.login(email=self.test_user.email, password=self.password)


class TestIndexView(LoggedInTestCase):

    def test_index_view(self):
        response = self.client.get(reverse_lazy("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/index.html")


class TestTalkRoomView(LoggedInTestCase):

    def test_talk_room_view(self):
        response = self.client.get(reverse_lazy("talk_room", args=[self.test_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/talk_room.html")


class TestSettingView(LoggedInTestCase):

    def test_setting_view(self):
        response = self.client.get(reverse_lazy("setting"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/setting.html")


class TestChangeUsernameView(LoggedInTestCase):

    def setUp(self):
        super().setUp()
        self.new_username = "new_testuser"

    def test_change_username(self):
        response = self.client.post(
            reverse_lazy("change_username"), {"username": self.new_username}
        )
        self.assertEqual(response.status_code, 302)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, self.new_username)


class TestChangeEmailView(LoggedInTestCase):

    def setUp(self):
        super().setUp()
        self.new_email = "new_email@example.com"

    def test_change_email(self):
        response = self.client.post(
            reverse_lazy("change_email"), {"email": self.new_email}
        )
        self.assertEqual(response.status_code, 302)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.email, self.new_email)


from django.core.files.uploadedfile import SimpleUploadedFile


class TestChangeImageView(LoggedInTestCase):

    def test_change_image(self):
        with open("media_local/211304.jpg", "rb") as img_file:
            uploaded_file = SimpleUploadedFile(
                "211304.jpg", img_file.read(), content_type="image/jpeg"
            )
        response = self.client.post(
            reverse_lazy("change_image"), {"image": uploaded_file}
        )

        self.assertEqual(response.status_code, 302)
        self.test_user.refresh_from_db()
        self.assertIsNotNone(self.test_user.image)


class TestDeleteUserView(LoggedInTestCase):

    def test_delete_user(self):
        response = self.client.post(reverse_lazy("delete_user"))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(id=self.test_user.id)
