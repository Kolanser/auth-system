from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from roles.models import AccessRule, Role


class AccessRuleInline(admin.TabularInline):
    model = AccessRule
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "element":
            kwargs["queryset"] = ContentType.objects.filter(app_label__in=["accounts", "roles"])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name", "description"]
    inlines = [AccessRuleInline]


@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    list_display = ["role", "element"]
    list_filter = ["role", "element"]
    search_fields = ["role__name", "element__model"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "element":
            kwargs["queryset"] = ContentType.objects.filter(app_label__in=["accounts", "roles"])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
