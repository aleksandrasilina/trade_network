from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("sellers/", include("sellers.urls", namespace="sellers")),
    path("users/", include("users.urls", namespace="users")),
    path("products/", include("products.urls", namespace="products")),
]
