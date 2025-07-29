from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательно')
        if not username:
            raise ValueError('Поле username обязательно')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=123, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name='Почта')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер'),
            (3, 'Бухгалтер'),
        ),
        default=1,
        verbose_name='Статус пользователя'
    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class OTPCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self, minutes=5):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=minutes)

    def __str__(self):
        return f"{self.user.email} — {self.code}"


class Favourite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    estate = models.ForeignKey('product.Estate', on_delete=models.CASCADE, verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
