import bcrypt
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from roles.models import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя"""

    email = models.EmailField(unique=True, verbose_name="email")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=150, blank=True, verbose_name="Отчество")

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата удаления")

    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль пользователя")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """Хеширование пароля с помощью bcrypt"""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, raw_password):
        """Проверка пароля"""
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))
