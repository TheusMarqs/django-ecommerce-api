from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60, unique=True)
    phone = models.CharField(max_length=15, unique=True)