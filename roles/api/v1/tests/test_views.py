from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.api.v1.tests.factory import UserFactory
from roles.api.v1.tests.factory import AccessRuleFactory, RoleFactory

User = get_user_model()


class RoleViewSetTest(APITestCase):
    def setUp(self):
        self.url_list = reverse("roles_api:role-list")
        self.user = UserFactory()

    def test_list_roles(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_roles_with_token(self):
        self.client.force_authenticate(user=self.user)
        role_admin = RoleFactory(name="Admin", is_admin=True)
        self.user.role = role_admin
        self.user.save()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        role_user = RoleFactory(name="User", is_admin=False)
        self.user.role = role_user
        self.user.save()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_role(self):
        role = RoleFactory()
        url_detail = reverse("roles_api:role-detail", args=[role.id])
        self.client.force_authenticate(user=self.user)
        role_admin = RoleFactory(name="Admin", is_admin=True)
        self.user.role = role_admin
        self.user.save()
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AccessRuleViewSetTest(APITestCase):
    def setUp(self):
        self.url_list = reverse("roles_api:access-rule-list")
        self.user = UserFactory()

    def test_list_access_rules(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_access_rules_with_token(self):
        self.client.force_authenticate(user=self.user)
        role_admin = RoleFactory(name="Admin", is_admin=True)
        self.user.role = role_admin
        self.user.save()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        role_user = RoleFactory(name="User", is_admin=False)
        self.user.role = role_user
        self.user.save()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_access_rule(self):
        access_rule = AccessRuleFactory(update_permission=False)
        url_detail = reverse("roles_api:access-rule-detail", args=[access_rule.id])
        self.client.force_authenticate(user=self.user)
        role_admin = RoleFactory(name="Admin", is_admin=True)
        self.user.role = role_admin
        self.user.save()
        data = {"update_permission": True}
        response = self.client.patch(url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_rule.refresh_from_db()
        self.assertEqual(access_rule.update_permission, True)
