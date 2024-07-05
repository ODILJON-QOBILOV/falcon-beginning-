from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView, CreateView,
    View, FormView, DetailView,
    ListView, CreateView
)
from apps.models import User, Product
from apps.forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout

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


class SignupView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'auth/register.html'
    success_url = "/"

class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            login(self.request, user)
            return redirect('/')
        
        return super().form_valid(form)
    

class UserLogoutView(View):
    def get(self, request):
        logout(self.request)
        return redirect('login')