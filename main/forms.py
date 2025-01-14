from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact
from .models import Customer
from .models import Merchant
from .models import Product

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
    phone = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class Delivery_ServiceForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'pix']
        
        
class MerchantProfileForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['first_name', 'last_name', 'company_name', 'company_registration', 'email', 'address', 'phone', 'pix']
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'type', 'model', 'slug', 'description', 'condition', 'color',
            'quantity', 'kilogram', 'availability', 'address', 'postcode',
            'price', 'promo_price', 'telephone1', 'telephone2', 'seller_name',
            'seller_email', 'website', 'message', 'carimg', 'is_vat_exempt',]

        # Adding widgets for better UI/UX and validation
        widgets = {
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Model'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Condition'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'kilogram': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)'}),
            'availability': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Availability'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'promo_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Promotional Price'}),
            'telephone1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Contact Number'}),
            'telephone2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Secondary Contact Number'}),
            'seller_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seller Name'}),
            'seller_emial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seller Name'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Seller Website'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Message'}),
            'carimg': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_vat_exempt': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'model': 'Product Model',
            'slug': 'Slug (for URLs)',
            'description': 'Product Description',
            'condition': 'Condition',
            'color': 'Color',
            'quantity': 'Quantity Available',
            'kilogram': 'Weight (kg)',
            'availability': 'Availability Status',
            'address': 'Seller Address',
            'postcode': 'Postcode',
            'price': 'Price',
            'promo_price': 'Promotional Price',
            'telephone1': 'Primary Phone',
            'telephone2': 'Secondary Phone',
            'seller_name': 'Seller Name',
            'seller_email': 'Seller Email',
            'website': 'Website URL',
            'message': 'Message',
            'carimg': 'Product Image',
            'is_vat_exempt': 'VAT Exempt (0%). Please ensure not to check the box for none exempted products',  # Label for the VAT exemption checkbox
        }

    # Overriding the form's save method to ensure the seller is set correctly
    def save(self, commit=True, seller=None):
        product = super().save(commit=False)
        if seller:  # Assign seller (must be a staff user)
            product.seller = seller
        if commit:
            product.save()
        return product        
 
        
