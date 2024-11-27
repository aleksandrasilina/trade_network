from django.db import models
from django_countries.fields import CountryField

from products.models import Product

NULLABLE = {"blank": True, "null": True}


class Contacts(models.Model):
    email = models.EmailField(verbose_name="Почта", help_text="Укажите почту")
    country = CountryField(verbose_name="Страна", help_text="Выберите страну")
    city = models.CharField(
        max_length=50, verbose_name="Город", help_text="Укажите город"
    )
    street = models.CharField(
        max_length=50, verbose_name="Улица", help_text="Укажите улицу"
    )
    house_number = models.CharField(
        max_length=50, verbose_name="Номер дома", help_text="Укажите номер дома"
    )

    def __str__(self):
        return f"{self.email} ({self.country}, {self.city})"

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class Seller(models.Model):
    # уровень в иерархии поставщиков, где 0 - это завод, 1 - следующее звено в цепочке поставок
    TRADE_NETWORK_LEVEL_CHOICES = (
        (
            0,
            0,
        ),
        (
            1,
            1,
        ),
        (
            2,
            2,
        ),
    )
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
    contacts = models.OneToOneField(
        Contacts,
        on_delete=models.SET_NULL,
        verbose_name="Контакты",
        help_text="Укажите контакты",
        related_name="contacts",
        **NULLABLE,
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Контакты",
        help_text="Укажите продукты",
        related_name="products",
        **NULLABLE,
    )
    supplier = models.OneToOneField(
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
        **NULLABLE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
    )
    trade_network_level = models.PositiveIntegerField(
        choices=TRADE_NETWORK_LEVEL_CHOICES,
        verbose_name="Уровень в торговой сети",
        help_text="Укажите уровень в торговой сети",
    )
    seller_type = models.CharField(
        max_length=30,
        choices=SELLER_TYPE_CHOICES,
        verbose_name="Тип продавца",
        help_text="Укажите тип продавца",
    )

    def __str__(self):
        return f"{self.seller_type} {self.name}"

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"
