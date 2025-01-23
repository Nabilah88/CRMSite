from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms

from .models import Orders
from .models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'profile_pic']
        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'

