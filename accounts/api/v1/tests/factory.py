import factory
from django.contrib.auth import get_user_model

from roles.api.v1.tests.factory import RoleFactory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    email = factory.Faker("email")
    password = factory.django.Password("pw")
    role = factory.SubFactory(RoleFactory)
