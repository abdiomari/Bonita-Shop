from django.db import models
from django.conf import settings
import uuid
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    SKU = models.CharField(max_length=255, unique=True, null=True, blank=True) 

    def save(self, *args, **kwargs):
        if not self.SKU:
            self.SKU = f'{self.category.name[:3]}-{self.name[:3]}-{uuid.uuid4().hex[:6]}'.upper()
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'{self.SKU} - {self.name} - {self.category} - KShs.{self.price} - {self.stock} in stock  - {self.isActive}'
    
    class Meta:
        verbose_name_plural = 'Products'

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name}  - {self.quantity}'
    
    class Meta:
        verbose_name_plural = 'Cart Items'
