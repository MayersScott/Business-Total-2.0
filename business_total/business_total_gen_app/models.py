from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    cost_price = models.FloatField()
    selling_price = models.FloatField()
    kol_d = models.FloatField()
    supplier_url = models.URLField(max_length=200, blank=True, null=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
