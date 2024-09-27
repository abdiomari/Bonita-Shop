from django.contrib import admin
from .models import Product, Category, CartItem

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('SKU', 'name', 'category', 'price', 'stock', 'isActive', 'created_at', 'updated_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(CartItem, CartItemAdmin)

