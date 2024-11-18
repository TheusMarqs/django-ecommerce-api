from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',  # Mapeia para o campo `product` no modelo
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, write_only=True)

    class Meta:
        model = Cart
        fields = ['id','user', 'total_value', 'items']
        read_only_fields = ['id','user', 'total_value']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(total_value=0)  # Criamos o carrinho vazio

        # Adiciona os itens no carrinho
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        # Calcula o total do carrinho
        cart.calculate_total()
        return cart
