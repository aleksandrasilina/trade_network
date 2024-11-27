from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from sellers.models import Seller
from sellers.serializers import SellerSerializer


class SellerViewSet(ModelViewSet):
    """Вьюсет для модели продавца."""

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
