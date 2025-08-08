from rest_framework import serializers
from decimal import Decimal
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'price_with_tax', 'category',]

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)
    
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price could not be negative...')
        return price