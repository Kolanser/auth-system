from django.contrib.auth import get_user_model
from rest_framework import serializers

from products.models import Order, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "product", "quantity", "user", "status", "created_at", "updated_at")
