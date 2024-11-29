from django.contrib import admin

from products.models import Product


@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model")
    list_display_links = ("name",)
    search_fields = ("name",)
