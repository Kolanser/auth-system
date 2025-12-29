import factory
from django.contrib.contenttypes.models import ContentType

from roles.models import AccessRule, Role


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Faker("name")


class ElementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContentType


class AccessRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessRule

    role = factory.SubFactory(RoleFactory)
    element = factory.SubFactory(ElementFactory)
