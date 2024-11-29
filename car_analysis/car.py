from django.db import models

class Car(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    prod_year = models.IntegerField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.prod_year})"
