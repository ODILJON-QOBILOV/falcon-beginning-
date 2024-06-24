from django.contrib import admin
from .models import Product, Category, ProductImage
# Register your models here.


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, )
    list_display = ('name', 'price', 'is_available')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)