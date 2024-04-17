from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from Store.models import Order

# Custom Forms
class CheckForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shippping_address','phone','payment_method'] 
