import factory

from accounts.api.v1.tests.factory import UserFactory
from products.models import Order, Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=10)
    user = factory.SubFactory(UserFactory)
