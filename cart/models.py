from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartItem')
    total_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def calculate_total(self):
        self.total_value = sum(item.quantity * item.product.price for item in self.cartitem_set.all())
        self.save()

@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"