from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
]



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=500)
    composition = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to Category model
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)  # Renamed from discount
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming each order is associated with a user
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the order
    total_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)  # Total price of the order
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')  # Order status field with choices
    # Add more fields as needed, such as shipping address, payment method, etc.

    def __str__(self):
        return f"Order #{self.pk} - {self.product.title}" if self.product else "Order"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart}"