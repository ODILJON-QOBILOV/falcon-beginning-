from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    specifications = models.JSONField(default=dict)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.quantity > 0


    @property
    def is_new(self):
        return now() - timedelta(days=7) < self.created_at


class ProductImage(BaseModel):
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name





class User(AbstractUser):
    class Type(models.TextChoices):
        USERS = "users", 'users'
        ADMIN = 'admin', 'admin'
        OPERATOR = 'operator', 'operator'
        MANAGER = 'manager', 'Manager'
    
    type = models.CharField(max_length=255, choices=Type.choices, default=Type.USERS)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)