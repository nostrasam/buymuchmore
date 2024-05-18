from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


# Create your models here.

class AppInfo(models.Model):
    appname = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo')
    carousel1 = models.ImageField(upload_to='carousel')
    carousel2 = models.ImageField(upload_to='carousel')
    carousel3 = models.ImageField(upload_to='carousel')
    banner = models.ImageField(upload_to='banner')
    copyright = models.IntegerField()
    
    def __str__(self):
        return self.appname
    

class Category(models.Model):
    brand = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    pix = models.ImageField(upload_to='pix')
        
    def __str__(self):
        return self.brand
    
class FeatureItem(models.Model):
    brand = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    pix = models.ImageField(upload_to='pix')
        
    def __str__(self):
        return self.brand
    
class Product(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    condition = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    availability = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    promo_price = models.IntegerField(blank=True, null=True)
    telephone1 = models.CharField(max_length=50)
    telephone2 = models.CharField(max_length=50, blank=True, null=True)
    seller_name = models.CharField(max_length=100)
    website = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    carimg = models.ImageField(upload_to='carimg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.model
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    pix = models.ImageField(upload_to='customer')
    
    def __str__(self):
        return self.user.username
    
    
class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    company_registration = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    pix = models.ImageField(upload_to='merchant')
    
    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    paid = models.BooleanField()
    amount = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username

 
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField()
    phone = models.CharField(max_length=50)
    pay_code = models.CharField(max_length=50)
    additional_info = models.TextField()
    payment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product} by {self.user}"
    
    
class Subscription(models.Model):
    brand = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    pix = models.ImageField(upload_to='pix')
        
    def __str__(self):
        return self.brand
    

class Subscribe(models.Model):
    type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    promo_price = models.IntegerField(blank=True, null=True)
    subcribeimg = models.ImageField(upload_to='subcribeimg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plan
    
    

    


