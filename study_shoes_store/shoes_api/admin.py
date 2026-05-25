from django.contrib import admin

from .models import Batch, Product, Client, Order

admin.site.register(Batch)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Order)