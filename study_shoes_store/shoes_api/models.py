from django.db import models
from django.contrib.auth.models import User


class Batch(models.Model):
    identifier_code = models.CharField(max_length=100)
    manufacturing_date = models.DateField()
    product_qty = models.IntegerField()
    
    def __str__(self):
        return self.identifier_code


class Product(models.Model):
    COLOUR_CHOICES = [
        ('red', 'Vermelho'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
        ('yellow', 'Amarelo'),
        ('orange', 'Laranja'),
        ('purple', 'Roxo'),
    ]
    identifier_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    batch_number = models.ForeignKey(Batch, on_delete=models.PROTECT)
    colour = models.CharField(max_length=20, choices=COLOUR_CHOICES, default='blue')
    description = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.identifier_code + ' - ' + self.name


class Client(models.Model):
    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.IntegerField(unique=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    order_date = models.DateField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return f'{self.order_number} - {self.total_value}'