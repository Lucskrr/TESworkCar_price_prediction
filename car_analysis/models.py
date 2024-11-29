from django.db import models

class Car(models.Model):
    id = models.AutoField(primary_key=True)  # Usando o AutoField, que é o comportamento padrão do Django
    price = models.IntegerField()
    levy = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    prod_year = models.IntegerField()
    category = models.CharField(max_length=100)
    leather_interior = models.BooleanField(default=False)
    fuel_type = models.CharField(max_length=50)
    engine_volume = models.FloatField(null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    cylinders = models.FloatField(null=True, blank=True)
    gear_box_type = models.CharField(max_length=50)
    drive_wheels = models.CharField(max_length=50)
    doors = models.IntegerField(null=True, blank=True)
    wheel = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    airbags = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.prod_year}) - ${self.price}"
