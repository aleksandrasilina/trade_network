from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from sellers.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    trade_network_level = SerializerMethodField(read_only=True)

    def get_trade_network_level(self, seller):
        """Возвращает уровень в иерархии поставщиков, где 0 - это завод, 1 - следующее звено в цепочке поставок."""
        if seller.supplier:
            if seller.supplier.supplier:
                return 2
            return 1
        return 0

    class Meta:
        model = Seller
        fields = "__all__"


class SellerUpdateSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновлений. Запрещает обновление через API поля «Задолженность перед поставщиком»."""

    class Meta:
        model = Seller
        exclude = ("debt",)
