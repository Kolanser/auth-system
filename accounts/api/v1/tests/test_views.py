from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.utils import generate_jwt

from .factory import UserFactory

User = get_user_model()


class UserRegistrationApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("accounts_api:registration")

    def test_register_user(self):
        data = {
            "first_name": "Фамильев",
            "last_name": "Имя",
            "patronymic": "Отчествович",
            "email": "email@email.ru",
            "password": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("accounts_api:login")
        self.user = UserFactory()
        self.password = "strongpassword123"
        self.user.set_password(self.password)
        self.user.save()

    def test_login_user(self):
        data = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(self.url, data=data)
        self.assertTrue(response.data.get("token"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileApiViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("accounts_api:profile")
        self.password = "strongpassword123"
        self.user = UserFactory(password=self.password)

    def test_get_user_not_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_with_token(self):
        token = generate_jwt(self.user)
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        token = generate_jwt(self.user)
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        data = {"first_name": "new_name"}
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])

    def test_delete_user(self):
        token = generate_jwt(self.user)
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_active, False)
