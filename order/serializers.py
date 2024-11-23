from rest_framework import serializers

from product.models import Product
from product.serializers import ProductSerializer
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    # product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation

class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id','client', 'date', 'order_items', 'total']
            
    def get_date(self, obj):
        # Retorne a data formatada como string
        return obj.date.strftime("%Y-%m-%d %H:%M:%S")
    
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(client=validated_data['client'], total=0.0)
        
        total = 0
        for item_data in order_items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total += product.price * quantity  # Supondo que o modelo Product tenha um campo `price`
        
        order.total = total
        order.save()
        return order
