from django.urls import include, path

urlpatterns = [
    path("v1/products/", include("products.api.v1.urls", namespace="products_v1")),
]
