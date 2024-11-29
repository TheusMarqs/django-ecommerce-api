from django.db import models
from product.models import Product
from django.contrib.auth.models import User
# from authentication.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartItem', blank=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total(self):
        total = sum(item.product.price * item.quantity for item in self.cart_items.all())
        self.total_value = total
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_delete, sender=CartItem)
def update_cart_on_item_delete(sender, instance, **kwargs):
    instance.cart.update_total()


@receiver(post_save, sender=CartItem)
def update_cart_on_item_save(sender, instance, **kwargs):
    instance.cart.update_total()