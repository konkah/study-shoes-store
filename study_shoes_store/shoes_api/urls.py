from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import BatchViewSet, ProductViewSet, ClientViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register(r'lotes_api', BatchViewSet)
router.register(r'produtos_api', ProductViewSet)
router.register(r'clientes_api', ClientViewSet)
router.register(r'pedidos_api', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]