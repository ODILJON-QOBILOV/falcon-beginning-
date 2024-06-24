from django.db import models
from datetime import timedelta
from django.utils.timezone import now

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





class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)