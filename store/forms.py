# forms.py
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'message']
        
        
from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    shipping_address = forms.CharField(label='Shipping Address', widget=forms.Textarea)
    billing_address = forms.CharField(label='Billing Address', widget=forms.Textarea)
    payment_method = forms.ChoiceField(label='Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    quantity = forms.IntegerField(label='Quantity', min_value=1)
    additional_comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)


class ShippingForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=10)
    country = forms.CharField(max_length=50)

# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',  # Specify the label for the 'email' field
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',  # Specify the label for the 'username' field
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        }
        

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, initial=1)


class UpdateCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=False)
    remove = forms.BooleanField(required=False)
