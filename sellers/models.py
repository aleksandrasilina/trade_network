from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

from products.models import Product

NULLABLE = {"blank": True, "null": True}


class Seller(models.Model):
    SELLER_TYPE_CHOICES = (
        (
            "factory",
            "завод",
        ),
        (
            "retail network",
            "розничная сеть",
        ),
        (
            "individual entrepreneur",
            "индивидуальный предприниматель",
        ),
    )

    name = models.CharField(
        max_length=100, verbose_name="Название", help_text="Укажите название"
    )
    email = models.EmailField(
        verbose_name="Почта",
        help_text="Укажите почту",
        **NULLABLE,
    )
    country = CountryField(
        verbose_name="Страна",
        help_text="Выберите страну",
        **NULLABLE,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Укажите город",
        **NULLABLE,
    )
    street = models.CharField(
        max_length=50,
        verbose_name="Улица",
        help_text="Укажите улицу",
        **NULLABLE,
    )
    house_number = models.CharField(
        max_length=50,
        verbose_name="Номер дома",
        help_text="Укажите номер дома",
        **NULLABLE,
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Продукты",
        help_text="Укажите продукты",
        related_name="products",
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Поставщик",
        help_text="Укажите поставщика",
        **NULLABLE,
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Задолженность",
        help_text="Укажите задолженность",
        default=0.00,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
    )
    seller_type = models.CharField(
        max_length=30,
        choices=SELLER_TYPE_CHOICES,
        verbose_name="Тип продавца",
        help_text="Укажите тип продавца",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"
