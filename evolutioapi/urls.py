from django.urls import path
from .views import orders_and_deliveries_by_brand, shipped_products

urlpatterns = [
    path('orders_and_deliveries_by_brand/', orders_and_deliveries_by_brand, name='orders_and_deliveries_by_brand'),
    path('shipped_products/', shipped_products, name='shipped_products'),
]
