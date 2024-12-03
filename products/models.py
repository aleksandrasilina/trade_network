from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Название", help_text="Укажите название продукта"
    )
    model = models.CharField(
        max_length=100, verbose_name="Модель", help_text="Укажите модель продукта"
    )
    released_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата выхода продукта на рынок",
        help_text="Укажите дату выхода продукта на рынок",
    )

    def __str__(self):
        return f"{self.name} {self.model}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
