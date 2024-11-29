from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from sellers.models import Seller
from sellers.serializers import SellerSerializer, SellerUpdateSerializer


class SellerViewSet(ModelViewSet):
    """Вьюсет для модели продавца."""

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("country",)

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return SellerUpdateSerializer
        return self.serializer_class
