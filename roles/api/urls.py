from django.urls import include, path

urlpatterns = [
    path("v1/roles/", include("roles.api.v1.urls", namespace="roles_v1")),
]
