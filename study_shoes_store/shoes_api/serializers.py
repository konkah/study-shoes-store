from rest_framework import serializers
from .models import Batch, Product, Client, Order
from validate_docbr import CPF


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = [
            "id",
            "identifier_code",
            "manufacturing_date",
            "product_qty",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "identifier_code",
            "name",
            "batch_number",
            "colour",
            "description",
            "value",
        ]


class ClientSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        data = super(ClientSerializer, self).to_representation(data)
        cpf = CPF()
        data["cpf"] = cpf.mask(data["cpf"])
        return data

    def to_internal_value(self, data):
        data = super(ClientSerializer, self).to_internal_value(data)
        data["cpf"] = data["cpf"].replace(".", "").replace("-", "")
        return data

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "cpf",
            "birth_date",
        ]

    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("Não é um CPF válido!")
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "client",
            "order_date",
            "seller",
            "products",
        ]

    def to_internal_value(self, data):
        data = super(OrderSerializer, self).to_internal_value(data)
        data["total_value"] = sum(p.value for p in data["products"])
        return data


class ListOrderSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        data = super(ListOrderSerializer, self).to_representation(data)

        first_name = data["seller"]["first_name"]
        last_name = data["seller"]["last_name"]
        username = data["seller"]["username"]
        data["seller"] = first_name + " " + last_name + " (" + username + ")"

        data["seller"] = data["seller"].strip()

        return data

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "client",
            "order_date",
            "seller",
            "products",
            "total_value",
        ]
        depth = 1
