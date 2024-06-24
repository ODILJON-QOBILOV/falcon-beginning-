from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product
from datetime import datetime

# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'product/products.html', {'products': products})


class ProductListView(ListView):
    datetime = datetime.now()
    model = Product 
    template_name = 'product/products.html'
    context_object_name = 'products'
    ordering = ['-id']



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-details.html'


class ProfileView(TemplateView):
    template_name = 'user/profile.html'


class SettingsView(TemplateView):
    template_name = 'user/settings.html'