from django.db import models
from django.utils import timezone

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    brand_id = models.IntegerField()
    customer_name = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    order_date = models.DateTimeField(default=timezone.now)
    price_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}"

class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Delivery(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipped = models.BooleanField()
    products = models.ManyToManyField(Product, through='DeliveryProduct')
    
    def __str__(self):
        return f"{self.id}"

class DeliveryProduct(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

