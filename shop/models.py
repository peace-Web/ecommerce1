from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    small_description = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField()
    status = models.BooleanField(default=0, help_text="0-default, 1-hidden")
    image = models.ImageField(upload_to="prod_images")
    original_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name} {self.quantity}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.selling_price * self.quantity

    def __str__(self) -> str:
        return f"{self.product.name} {self.quantity}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    address = models.TextField()
    zipcode = models.IntegerField()
    total = models.IntegerField()
    payment_mode = models.CharField(max_length=100, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    tracking_no = models.CharField(max_length=150)
    orderstatus = (
        ("Pending","Pending"),
        ("Out For Delivery", "Out For Delivery"),
        ("Completed", "Completed")
    )
    status = models.CharField(max_length=50, choices=orderstatus, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)

    def __str__(self) -> str:
        return '{} - {}'.format(self.order.id, self.order.tracking_no)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    caption = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="user_images", null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username