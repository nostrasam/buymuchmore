from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact
from .models import Customer
from .models import Merchant


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'message', 'email', 'telephone', 'address']
        
        
class CustomerForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class MerchantForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'pix']
        
        
class MerchantProfileForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['first_name', 'last_name', 'company_name', 'company_registration', 'email', 'address', 'phone', 'pix']
        

        
 
        
