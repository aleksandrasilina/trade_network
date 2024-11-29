from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html

from sellers.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "seller_type",
        "city",
        "link_to_supplier",
        "trade_network_level",
        "debt",
    )
    list_filter = ("city", "seller_type")
    search_fields = ("name", "email")
    list_display_links = ("name",)
    list_select_related = ("supplier",)
    actions = ("clear_debt",)

    def link_to_supplier(self, obj):
        """Возвращает ссылку на поставщика."""
        if obj.supplier is not None:
            link = reverse("admin:sellers_seller_change", args=[obj.supplier.id])
            return format_html(
                '<a href="{}">{}</a>',
                link,
                obj.supplier,
            )

    link_to_supplier.short_description = "Поставщик"

    @admin.action(description="Обнулить задолженность")
    def clear_debt(self, request, queryset):
        """Очищает задолженность перед поставщиком."""

        queryset.update(debt=0)
        messages.success(request, "Задолженность успешно обнулена!")
