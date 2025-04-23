from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()


class Payment(models.Model):
    """Модель для хранения информации о донатах."""

    user = models.ForeignKey(User, verbose_name="Донатер", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="Сумма", max_digits=10, decimal_places=2)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    collection = models.ForeignKey(
        "Collection",
        verbose_name="Сбор",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    is_hidden = models.BooleanField(verbose_name="Сумма скрыта", default=False)

    def __str__(self):
        return f"({self.date}) Донат на {self.amount} от {self.user.username}"


class Collection(models.Model):
    """Модель для хранения информации о сборах."""

    class Causes(models.TextChoices):
        WEDDING = "WD", "Свадьба"
        BIRTHDAY = "BD", "День рождения"
        FUNERAL = "FN", "Похороны"

    author = models.ForeignKey(
        User, verbose_name="Автор сбора", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)
    cause = models.CharField(
        verbose_name="Повод", max_length=255, choices=Causes.choices
    )
    target_amount = models.DecimalField(
        verbose_name="Цель", max_digits=10, decimal_places=2
    )
    cover_image = models.ImageField(verbose_name="Обложка", upload_to="cover_images/")
    due_date = models.DateTimeField(
        verbose_name="Дата завершения", null=True, blank=True
    )

    def __str__(self):
        return f"Сбор от {self.author.username} на {self.name} ({self.cause})"

    @property
    @admin.display(description="Уникальных донатеров")
    def participant_count(self):
        return self.payments.values("user").distinct().count()

    @property
    @admin.display(description="Собрано")
    def current_amount(self):
        return sum(payment.amount for payment in self.payments.all())
