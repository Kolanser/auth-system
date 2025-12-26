from django.urls import include, path
from rest_framework.routers import DefaultRouter

from roles.api.v1.views import AccessRuleViewSet, ElementListApiView, RoleViewSet

app_name = "roles_api"

router = DefaultRouter()
router.register(r"access-rules", AccessRuleViewSet, basename="access-rule")
router.register(r"", RoleViewSet, basename="role")

urlpatterns = [
    path("elements/", ElementListApiView.as_view(), name="element-content_type"),
    path("", include(router.urls)),
]
