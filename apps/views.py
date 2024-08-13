from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView, CreateView,
    View, FormView, DetailView,
    ListView, CreateView
)
from apps.models import User, Product, WishList
from apps.forms import UserRegisterForm, UserLoginForm, OrdersForm
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

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('qidiruv')
        if search is not None and len(search) > 0:
            qs = qs.filter(name__icontains=search)
        return qs


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-details.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = OrdersForm()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = OrdersForm(request.POST)
        if form.is_valid():
            # Create and save the order
            order = form.save(commit=False)
            order.product = self.object
            order.save()
            # Redirect to a success page or another appropriate place
            return redirect('success_url')  # Replace with your success URL or redirect to the same page

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class ProfileView(TemplateView):
    template_name = 'user/profile.html'


class SettingsView(TemplateView, LoginRequiredMixin):
    model = User
    template_name = 'user/settings.html'


class SignupView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'auth/register.html'
    success_url = "/"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


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


class WishlistTemplateView(ListView):
    template_name = 'product/shopping-cart.html'
    model = WishList
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


class WishListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        pk = kwargs.get('pk')
        product = Product.objects.filter(id=pk).first()
        if user and pk:
            wishlist = WishList.objects.filter(product=product).exists()
            if not wishlist:
                WishList.objects.create(
                    user=user,
                    product=product
                )
            else:
                wishlist = WishList.objects.filter(product=product).first()
                wishlist.delete()
        return redirect('/')