from django.contrib import admin
from .models import Product, Cart, OrderItem, Order, Customer
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)