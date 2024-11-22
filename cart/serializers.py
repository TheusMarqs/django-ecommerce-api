from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import Cart, CartItem
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'cart_items', 'total_value']