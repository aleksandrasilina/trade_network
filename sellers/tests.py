from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from sellers.models import Seller
from users.models import User


class SellerTestCase(APITestCase):
    """Класс для тестирования продукта."""

    def setUp(self):
        """Метод для заполнения первичных данных."""

        # создаем админа
        self.admin_user = User.objects.create(email="admin@email.com", is_staff=True)

        # создаем обычного пользователя
        self.regular_user = User.objects.create(email="regular_user@email.com")

        # создаем продукт
        self.product = Product.objects.create(
            name="test1",
            model="1",
        )

        # создаем продавца
        self.seller = Seller.objects.create(
            name="test1",
            country="RU",
            seller_type="factory",
        )
        self.seller.products.set([self.product])

    # Тесты для админа
    def test_seller_retrieve_admin_access(self):
        """Тестирует получение информации о продавце админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("products"), [product.pk for product in self.seller.products.all()]
        )

    def test_seller_create_admin_access(self):
        """Тестирует создание продавца админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("sellers:seller-list")
        data = {
            "name": "test2",
            "country": "CN",
            "products": [self.product.pk],
            "seller_type": "individual entrepreneur",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seller.objects.all().count(), 2)

    def test_seller_update_admin_access(self):
        """Тестирует обновление информации о продавце админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        data = {"seller_type": "retail network"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("seller_type"), "retail network")

    def test_seller_delete_admin_access(self):
        """Тестирует удаление продавца админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seller.objects.all().count(), 0)

    def test_seller_list_admin_access(self):
        """Тестирует получение списка продавцов админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("sellers:seller-list")
        response = self.client.get(url)
        data = response.json()

        result = [
            {
                "id": self.seller.pk,
                "trade_network_level": 0,
                "name": self.seller.name,
                "email": None,
                "country": self.seller.country,
                "city": None,
                "street": None,
                "house_number": None,
                "debt": "0.00",
                "created_at": self.seller.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "seller_type": self.seller.seller_type,
                "supplier": None,
                "products": [self.product.pk],
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # # Тесты для обычного пользователя
    def test_seller_retrieve_regular_user(self):
        """Тестирует получение информации о продавце обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("products"), [product.pk for product in self.seller.products.all()]
        )

    def test_seller_create_regular_user(self):
        """Тестирует создание продавца обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("sellers:seller-list")
        data = {
            "name": "test2",
            "country": "CN",
            "products": [self.product.pk],
            "seller_type": "individual entrepreneur",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seller.objects.all().count(), 2)

    def test_seller_update_regular_user(self):
        """Тестирует обновление информации о продавце обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        data = {"seller_type": "retail network"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("seller_type"), "retail network")

    def test_seller_delete_regular_user(self):
        """Тестирует удаление продавца обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seller.objects.all().count(), 0)

    def test_seller_list_regular_user(self):
        """Тестирует получение списка продавцов обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("sellers:seller-list")
        response = self.client.get(url)
        data = response.json()

        result = [
            {
                "id": self.seller.pk,
                "trade_network_level": 0,
                "name": self.seller.name,
                "email": None,
                "country": self.seller.country,
                "city": None,
                "street": None,
                "house_number": None,
                "debt": "0.00",
                "created_at": self.seller.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "seller_type": self.seller.seller_type,
                "supplier": None,
                "products": [self.product.pk],
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для анонимного пользователя
    def test_seller_retrieve_anonymous_user_access(self):
        """Тестирует получение информации о продукте анонимным пользователем."""

        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        response = self.client.get(url)
        response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_seller_create_anonymous_user_access(self):
        """Тестирует создание продукта анонимным пользователем."""

        url = reverse("sellers:seller-list")
        data = {
            "name": "test2",
            "country": "CN",
            "products": [self.product.pk],
            "seller_type": "individual entrepreneur",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_seller_update_anonymous_user_access(self):
        """Тестирует обновление информации о продукте анонимным пользователем."""

        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        data = {"seller_type": "retail network"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_seller_delete_anonymous_user_access(self):
        """Тестирует удаление продукта анонимным пользователем."""

        url = reverse("sellers:seller-detail", args=(self.seller.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_seller_list_anonymous_user_access(self):
        """Тестирует получение списка продуктов анонимным пользователем."""

        url = reverse("sellers:seller-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
