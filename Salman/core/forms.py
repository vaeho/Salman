from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BusinessUser


class BusinessUserCreationForm(UserCreationForm):
    class Meta:
        model = BusinessUser
        fields = ['business_name', 'username', 'email', 'phone_number', 'address', 'password1', 'password2']

class BusinessUserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)



