from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

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
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
