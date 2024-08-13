from apps.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Orders

class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('parollar mos emas!')
        print(password)
        return make_password(password)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['fullname', 'phone']