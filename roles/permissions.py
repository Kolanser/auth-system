from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from .models import AccessRule


class AccessRulePermission(permissions.BasePermission):
    def __init__(self, action=None, scope="own"):
        """
        :param action: 'read', 'create', 'update', 'delete'
        :param scope: 'own' или 'all'
        """
        self.action = action
        self.scope = scope

    def has_permission(self, request, view):
        user_role = request.user.role
        if user_role and user_role.is_admin:
            return True

        model = self._get_model_from_view(view)
        if not model:
            return False

        action = self.action or self._map_action(request.method)

        content_type = ContentType.objects.get_for_model(model)

        if not user_role:
            return False

        try:
            rule = AccessRule.objects.get(role=user_role, element=content_type)
        except AccessRule.DoesNotExist:
            return False

        return self._check_permission_for_action(rule, action, self.scope)

    def has_object_permission(self, request, view, obj):
        user_role = request.user.role
        if user_role.is_admin:
            return True

        model = obj.__class__
        content_type = ContentType.objects.get_for_model(model)

        if not user_role:
            return False

        try:
            rule = AccessRule.objects.get(role=user_role, element=content_type)
        except AccessRule.DoesNotExist:
            return False

        action = self.action or self._map_action(request.method)

        if action == "read":
            if rule.read_all_permission:
                return True
            elif rule.read_permission:
                return self._check_ownership(request.user, obj)

        elif action == "update":
            if rule.update_all_permission:
                return True
            elif rule.update_permission:
                return self._check_ownership(request.user, obj)

        elif action == "delete":
            if rule.delete_all_permission:
                return True
            elif rule.delete_permission:
                return self._check_ownership(request.user, obj)

        return False

    def _get_model_from_view(self, view):
        if hasattr(view, "queryset"):
            return view.queryset.model
        elif hasattr(view, "model"):
            return view.model
        elif hasattr(view, "get_queryset"):
            return view.get_queryset().model
        return None

    def _map_action(self, method):
        method_map = {
            "GET": "read",
            "HEAD": "read",
            "OPTIONS": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete",
        }
        return method_map.get(method, "read")

    def _check_permission_for_action(self, rule, action, scope):
        if action == "read":
            if scope == "all":
                return rule.read_all_permission
            return rule.read_permission or rule.read_all_permission

        elif action == "create":
            return rule.create_permission

        elif action == "update":
            if scope == "all":
                return rule.update_all_permission
            return rule.update_permission or rule.update_all_permission

        elif action == "delete":
            if scope == "all":
                return rule.delete_all_permission
            return rule.delete_permission or rule.delete_all_permission

        return False

    def _check_ownership(self, user, obj):
        owner_field = "user"

        if hasattr(obj, owner_field):
            return obj.owner_field == user
        return False


class CanReadPermission(AccessRulePermission):
    """Может читать свои объекты"""

    def __init__(self):
        super().__init__(action="read", scope="own")


class CanReadAllPermission(AccessRulePermission):
    """Может читать все объекты"""

    def __init__(self):
        super().__init__(action="read", scope="all")


class CanCreatePermission(AccessRulePermission):
    """Может создавать объекты"""

    def __init__(self):
        super().__init__(action="create")


class CanUpdatePermission(AccessRulePermission):
    """Может обновлять свои объекты"""

    def __init__(self):
        super().__init__(action="update", scope="own")


class CanUpdateAllPermission(AccessRulePermission):
    """Может обновлять все объекты"""

    def __init__(self):
        super().__init__(action="update", scope="all")


class CanDeletePermission(AccessRulePermission):
    """Может удалять свои объекты"""

    def __init__(self):
        super().__init__(action="delete", scope="own")


class CanDeleteAllPermission(AccessRulePermission):
    """Может удалять все объекты"""

    def __init__(self):
        super().__init__(action="delete", scope="all")


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role and request.user.role.is_admin
