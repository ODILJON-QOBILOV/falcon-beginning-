from django.core.mail import send_mail

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


    def save(self, commit=True):
        print('shu yerda xato')
        user = super().save(commit)
        send_mail(
            subject='Welcome',
            message='message to registeres user',
            from_email='temirovv21@gmail.com',
            recipient_list=[user.email],
        )
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['fullname', 'phone']