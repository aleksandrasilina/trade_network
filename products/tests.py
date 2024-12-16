from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from users.models import User


class ProductTestCase(APITestCase):
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

    # Тесты для админа
    def test_product_retrieve_admin_access(self):
        """Тестирует получение информации о продукте админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("products:product-detail", args=(self.product.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.product.name)

    def test_product_create_admin_access(self):
        """Тестирует создание продукта админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("products:product-list")
        data = {
            "name": "test2",
            "model": "2",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_update_admin_access(self):
        """Тестирует обновление информации о продукте админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("products:product-detail", args=(self.product.pk,))
        data = {"model": "11"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("model"), "11")

    def test_product_delete_admin_access(self):
        """Тестирует удаление продукта админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("products:product-detail", args=(self.product.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_product_list_admin_access(self):
        """Тестирует получение списка продуктов админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("products:product-list")
        response = self.client.get(url)
        data = response.json()

        result = [
            {
                "id": self.product.pk,
                "name": self.product.name,
                "model": self.product.model,
                "released_at": self.product.released_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для обычного пользователя
    def test_product_retrieve_regular_user(self):
        """Тестирует получение информации о продукте обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("products:product-detail", args=(self.product.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.product.name)

    def test_product_create_regular_user(self):
        """Тестирует создание продукта обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("products:product-list")
        data = {
            "name": "test2",
            "model": "2",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_update_regular_user(self):
        """Тестирует обновление информации о продукте обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("products:product-detail", args=(self.product.pk,))
        data = {"model": "11"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("model"), "11")

    def test_product_delete_regular_user(self):
        """Тестирует удаление продукта обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("products:product-detail", args=(self.product.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_product_list_regular_user(self):
        """Тестирует получение списка продуктов обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("products:product-list")
        response = self.client.get(url)
        data = response.json()

        result = [
            {
                "id": self.product.pk,
                "name": self.product.name,
                "model": self.product.model,
                "released_at": self.product.released_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для анонимного пользователя
    def test_product_retrieve_anonymous_user_access(self):
        """Тестирует получение информации о продукте анонимным пользователем."""

        url = reverse("products:product-detail", args=(self.product.pk,))
        response = self.client.get(url)
        response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_create_anonymous_user_access(self):
        """Тестирует создание продукта анонимным пользователем."""

        url = reverse("products:product-list")
        data = {
            "name": "test2",
            "model": "2",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_update_anonymous_user_access(self):
        """Тестирует обновление информации о продукте анонимным пользователем."""

        url = reverse("products:product-detail", args=(self.product.pk,))
        data = {"model": "11"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_delete_anonymous_user_access(self):
        """Тестирует удаление продукта анонимным пользователем."""

        url = reverse("products:product-detail", args=(self.product.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_list_anonymous_user_access(self):
        """Тестирует получение списка продуктов анонимным пользователем."""

        url = reverse("products:product-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class MyModelSerializerTest(TestCase):
#     def test_serializer_valid_data(self):
#         data = {'field1': 'value1', 'field2': 'value2'}
#         serializer = ProductSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
