from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
