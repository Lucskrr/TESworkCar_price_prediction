from django.urls import path
from .views import car_list, car_price_dashboard, predict_car_price, index

urlpatterns = [
    path('', index, name='index'),  # Página inicial
    path('car-list/', car_list, name='car_list'),  # Lista de carros usando a função car_list
    path('car-analysis/', car_price_dashboard, name='car_analysis'),  # Análise de carros
    path('predict-price/', predict_car_price, name='predict_price'),  # Predição de preço
]
