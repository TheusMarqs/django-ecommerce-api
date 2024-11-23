from django.db import models
from django.contrib.auth.models import User

from product.models import Product

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem', blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"