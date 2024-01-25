from django.contrib import admin
from .models import Order, Delivery, Product

class ProductInline(admin.TabularInline):
    model = Product

class DeliveryProductInline(admin.TabularInline):
    model = Delivery.products.through

class DeliveryInline(admin.TabularInline):
    model = Delivery
    inlines = [DeliveryProductInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [DeliveryInline]

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    inlines = [DeliveryProductInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
