from django.contrib.contenttypes.models import ContentType
from django.db import models


class Role(models.Model):
    """Роли пользователей"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Название роли")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    """Правила доступа для ролей"""

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="access_rules", verbose_name="Роль")
    element = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Элемент правила доступа",
        help_text="Модель, к которой применимо правило доступа",
    )

    read_permission = models.BooleanField(default=False, verbose_name="Чтение своих")
    read_all_permission = models.BooleanField(default=False, verbose_name="Чтение всех")
    create_permission = models.BooleanField(default=False, verbose_name="Создание")
    update_permission = models.BooleanField(default=False, verbose_name="Обновление своих")
    update_all_permission = models.BooleanField(default=False, verbose_name="Обновление всех")
    delete_permission = models.BooleanField(default=False, verbose_name="Удаление своих")
    delete_all_permission = models.BooleanField(default=False, verbose_name="Удаление всех")

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        constraints = [
            models.UniqueConstraint(fields=["element", "role"], name=("unique_role_for_element")),
        ]

    def __str__(self):
        return f"{self.role.name} -> {self.element.model}"
