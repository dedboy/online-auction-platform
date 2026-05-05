from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product, User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number'] # phone_number modelingizda bor ekan

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # start_time ni ham qo'shdik, chunki modelingizda u majburiy (null=True emas)
        fields = ['category', 'title', 'description', 'start_price', 'start_time', 'end_time', 'image']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }