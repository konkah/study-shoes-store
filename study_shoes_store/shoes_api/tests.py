from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from decimal import Decimal

from .models import Batch, Product, Client, Order
from .serializers import ClientSerializer, OrderSerializer


class ClientSerializerTestCase(TestCase):
    """Test CPF validation and formatting in ClientSerializer"""

    def test_valid_cpf_accepted(self):
        """Valid CPF should be accepted and stored without formatting"""
        data = {
            "name": "João Silva",
            "cpf": "462.324.520-97",  # formatted input (valid CPF)
            "birth_date": date(1990, 1, 1),
        }
        serializer = ClientSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        # CPF should be stored without formatting
        self.assertEqual(serializer.validated_data["cpf"], "46232452097")

    def test_invalid_cpf_rejected(self):
        """Invalid CPF should be rejected with validation error"""
        data = {
            "name": "João Silva",
            "cpf": "111.111.111-11",  # invalid CPF (all same digits)
            "birth_date": date(1990, 1, 1),
        }
        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cpf", serializer.errors)

    def test_cpf_formatting_output(self):
        """CPF should be formatted in output representation"""
        client = Client.objects.create(
            name="João Silva",
            cpf="46232452097",  # unformatted (valid CPF)
            birth_date=date(1990, 1, 1),
        )
        serializer = ClientSerializer(client)
        # Should output formatted CPF
        self.assertEqual(serializer.data["cpf"], "462.324.520-97")

    def test_cpf_unique_constraint(self):
        """CPF must be unique across clients"""
        Client.objects.create(
            name="João",
            cpf="46232452097",
            birth_date=date(1990, 1, 1),
        )
        # Try creating another with same CPF
        data = {
            "name": "Maria",
            "cpf": "2.324.520-97",
            "birth_date": date(1995, 5, 5),
        }
        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cpf", serializer.errors)


class OrderSerializerTestCase(TestCase):
    """Test Order total_value calculation in OrderSerializer"""

    def setUp(self):
        """Create test data"""
        self.batch = Batch.objects.create(
            identifier_code="BATCH001",
            manufacturing_date=date(2024, 1, 1),
            product_qty=100,
        )
        self.product1 = Product.objects.create(
            identifier_code="PROD001",
            name="Sapato A",
            batch_number=self.batch,
            colour="red",
            description="Sapato vermelho",
            value=Decimal("100.50"),
        )
        self.product2 = Product.objects.create(
            identifier_code="PROD002",
            name="Sapato B",
            batch_number=self.batch,
            colour="blue",
            description="Sapato azul",
            value=Decimal("200.75"),
        )
        self.client = Client.objects.create(
            name="João Silva",
            cpf="12345678910",
            birth_date=date(1990, 1, 1),
        )
        self.seller = User.objects.create_user(
            username="vendedor",
            password="senha123",
        )

    def test_order_total_value_calculation(self):
        """Order total_value should sum product values correctly"""
        data = {
            "order_number": 1,
            "client": self.client.id,
            "order_date": date(2024, 6, 1),
            "seller": self.seller.id,
            "products": [self.product1.id, self.product2.id],
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # total_value should be sum of product1.value + product2.value
        expected_total = Decimal("100.50") + Decimal("200.75")
        self.assertEqual(
            serializer.validated_data["total_value"],
            expected_total,
        )

    def test_order_total_value_single_product(self):
        """Order with single product should calculate correct total"""
        data = {
            "order_number": 2,
            "client": self.client.id,
            "order_date": date(2024, 6, 1),
            "seller": self.seller.id,
            "products": [self.product1.id],
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["total_value"],
            Decimal("100.50"),
        )

    def test_order_number_unique_constraint(self):
        """Order number must be unique"""
        Order.objects.create(
            order_number=1,
            client=self.client,
            order_date=date(2024, 6, 1),
            total_value=Decimal("100.00"),
            seller=self.seller,
        )
        data = {
            "order_number": 1,  # same order number
            "client": self.client.id,
            "order_date": date(2024, 6, 2),
            "seller": self.seller.id,
            "products": [self.product1.id],
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("order_number", serializer.errors)


class APIAuthenticationTestCase(APITestCase):
    """Test authentication requirements on API endpoints"""

    def setUp(self):
        """Create test user and data"""
        self.user = User.objects.create_user(
            username="admin",
            password="admin",
        )
        self.batch = Batch.objects.create(
            identifier_code="BATCH001",
            manufacturing_date=date(2024, 1, 1),
            product_qty=100,
        )

    def test_client_list_without_auth_denied(self):
        """GET /clientes_api/ without auth should return 403"""
        response = self.client.get("/clientes_api/")
        self.assertIn(response.status_code, [401, 403])

    def test_client_list_with_auth_allowed(self):
        """GET /clientes_api/ with auth should return 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/clientes_api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_batch_list_without_auth_denied(self):
        """GET /lotes_api/ without auth should return 403"""
        response = self.client.get("/lotes_api/")
        self.assertIn(response.status_code, [401, 403])

    def test_batch_list_with_auth_allowed(self):
        """GET /lotes_api/ with auth should return 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/lotes_api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_without_auth_denied(self):
        """GET /produtos_api/ without auth should return 403"""
        response = self.client.get("/produtos_api/")
        self.assertIn(response.status_code, [401, 403])

    def test_product_list_with_auth_allowed(self):
        """GET /produtos_api/ with auth should return 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/produtos_api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_without_auth_denied(self):
        """GET /pedidos_api/ without auth should return 403"""
        response = self.client.get("/pedidos_api/")
        self.assertIn(response.status_code, [401, 403])

    def test_order_list_with_auth_allowed(self):
        """GET /pedidos_api/ with auth should return 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/pedidos_api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
