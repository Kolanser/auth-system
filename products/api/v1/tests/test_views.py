from random import randint

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.api.v1.tests.factory import UserFactory
from products.api.v1.tests.factory import ProductFactory
from roles.api.v1.tests.factory import AccessRuleFactory, RoleFactory


class ProductListViewTest(APITestCase):
    def setUp(self):
        self.url_list = reverse("products_api:product-list")
        self.url_detail = lambda id: reverse("products_api:product-detail", args=[id])
        self.element = ContentType.objects.get(app_label="products", model="product")
        self.count_products = randint(3, 44)
        self.products = ProductFactory.create_batch(self.count_products)

    def test_get_products_without_auth(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_products_with_auth(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        role_manager = RoleFactory(name="manager", is_admin=False)
        user.role = role_manager
        user.save()
        AccessRuleFactory(
            role=role_manager,
            element=self.element,
            read_all_permission=True,
            read_permission=True,
        )
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url_detail(self.products[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_products_from_user(self):
        user = UserFactory()
        role_user = RoleFactory(name="user", is_admin=False)
        user.role = role_user
        user.save()
        AccessRuleFactory(role=role_user, element=self.element, create_permission=False)
        data = {"name": "Test Product", "price": "99.99"}
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_update_delete_products_from_manager(self):
        user = UserFactory()
        role_manager = RoleFactory(name="manager", is_admin=False)
        user.role = role_manager
        user.save()
        acces_rule = AccessRuleFactory(role=role_manager, element=self.element, create_permission=True)
        data = {"name": "Test Product", "price": "99.99"}
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url_list, data=data)
        product_id = response.data["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_data = {"name": "Updated Product", "price": "79.99"}
        response = self.client.put(self.url_detail(product_id), data=new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        acces_rule.update_all_permission = True
        acces_rule.save()
        response = self.client.put(self.url_detail(product_id), data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_data["name"])

        response = self.client.delete(self.url_detail(product_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        acces_rule.delete_all_permission = True
        acces_rule.save()
        response = self.client.delete(self.url_detail(product_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
