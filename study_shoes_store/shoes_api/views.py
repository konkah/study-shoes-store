from .models import Batch, Product, Client, Order
from .serializers import BatchSerializer, ProductSerializer, ClientSerializer, OrderSerializer, ListOrderSerializer
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    ordering_fields = ['total_value', 'order_date']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ListOrderSerializer
        return OrderSerializer