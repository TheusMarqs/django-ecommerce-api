from django.db import models
from category.models import Category

class Supplier(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name