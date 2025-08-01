# Generated by Django 5.2.4 on 2025-07-29 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("username", models.CharField(max_length=123, verbose_name="Имя")),
                (
                    "email",
                    models.EmailField(
                        default=None, max_length=254, unique=True, verbose_name="Почта"
                    ),
                ),
                (
                    "created_date",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Обычный пользователь"),
                            (2, "Менеджер"),
                            (3, "Бухгалтер"),
                        ],
                        default=1,
                        verbose_name="Статус пользователя",
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
