import os
import django
from django.test import TestCase
from .models import Car

# Configurar o Django manualmente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_price_prediction.settings')
django.setup()

class CarModelTest(TestCase):
    def setUp(self):
        """Configuração inicial do teste: Criação de um carro"""
        Car.objects.create(manufacturer="Toyota", model="Corolla", prod_year=2020, price=50000)

    def test_car_creation(self):
        """Verifica se o carro foi criado corretamente"""
        car = Car.objects.get(manufacturer="Toyota")
        self.assertEqual(car.model, "Corolla")

    def test_car_price(self):
        """Verifica se o preço do carro está correto"""
        car = Car.objects.get(manufacturer="Toyota")
        self.assertEqual(car.price, 50000)

    def test_invalid_car(self):
        """Verifica se buscar um carro inexistente gera uma exceção"""
        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(manufacturer="Invalid")
