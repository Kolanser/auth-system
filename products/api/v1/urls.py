from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, ProductViewSet

app_name = "products_api"

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
