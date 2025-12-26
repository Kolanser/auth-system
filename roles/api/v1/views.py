from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from roles.api.v1.serializers import AccessRuleSerializer, ContentTypeSerializer, RoleSerializer
from roles.models import AccessRule, Role
from roles.permissions import IsAdmin

User = get_user_model()


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]


class AccessRuleViewSet(viewsets.ModelViewSet):
    serializer_class = AccessRuleSerializer
    queryset = AccessRule.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]


class ElementListApiView(ListAPIView):
    serializer_class = ContentTypeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return ContentType.objects.filter(
            app_label__in=["accounts", "roles", "products"], model__in=["user", "role", "product", "order"]
        )
