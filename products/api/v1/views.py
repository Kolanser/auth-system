from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from products.api.v1.serializers import OrderSerializer, ProductSerializer
from products.models import Order, Product
from roles.models import AccessRule
from roles.permissions import CanCreatePermission, CanDeletePermission, CanReadPermission, CanUpdatePermission


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated, CanReadPermission]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, CanCreatePermission]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, CanUpdatePermission]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, CanDeletePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated, CanReadPermission]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, CanCreatePermission]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, CanUpdatePermission]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, CanDeletePermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not getattr(self.request.user.role, "is_admin", False):

            content_type = ContentType.objects.get_for_model(Order)

            try:
                rule = AccessRule.objects.get(role=self.request.user.role, element=content_type)
                if rule.read_permission and not rule.read_all_permission:
                    queryset = queryset.filter(user=self.request.user)
            except AccessRule.DoesNotExist:
                queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
