from django.contrib import admin
from .models import Product, Order, Category, ContactMessage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ContactMessage)
