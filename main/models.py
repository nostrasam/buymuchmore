from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.utils.timezone import now



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
    sponsorname = models.CharField(max_length=50)
    website = models.URLField(default='a')
    pix = models.ImageField(upload_to='pix')
        
    def __str__(self):
        return self.brand
    
class Product(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})  # Only staff users can be sellers
    model = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    condition = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    kilogram = models.FloatField()
    availability = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_price = models.IntegerField(blank=True, null=True)
    telephone1 = models.CharField(max_length=50)
    telephone2 = models.CharField(max_length=50, blank=True, null=True)
    seller_name = models.CharField(max_length=100)
    website = models.CharField(max_length=50, blank=True, null=True)
    seller_email = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    carimg = models.ImageField(upload_to='carimg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating_value = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    is_vat_exempt = models.BooleanField(default=False, help_text="Select if this product is VAT exempt (0%).")
    total_views = models.PositiveIntegerField(default=0)  # Total views for the product
    total_customers = models.PositiveIntegerField(default=1)  # Total unique customers for the product, default is 1 to avoid division by zero
    ingredients = models.TextField()
    instructions = models.TextField()


    # New method to get views per customer
    def get_views_per_customer(self):
        if self.total_customers > 0:
            return self.total_views / self.total_customers
        return 0.0
    # Existing get_average_rating method
    def get_average_rating(self):
        if self.rating_count > 0:
            return self.rating_value / self.rating_count
        return 0.0

    def __str__(self):
        return self.model
    
class FeatureProduct(models.Model):
    type = models.ForeignKey(FeatureItem, on_delete=models.CASCADE)
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
    email = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    carimg = models.ImageField(upload_to='carimg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.model
    

class CustomerHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product}"
    
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
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    pix = models.ImageField(upload_to='customer')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.user.username
     
class Merchant(models.Model):
    SELLER_ADDRESS = 'seller'
    DELIVERY_SERVICE_ADDRESS = 'delivery'
    ADDRESS_CHOICES = [
        (SELLER_ADDRESS, 'Seller Address'),
        (DELIVERY_SERVICE_ADDRESS, 'Delivery Service Address'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    company_registration = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=150)
    address_type = models.CharField(
        max_length=8,
        choices=ADDRESS_CHOICES,
        default=SELLER_ADDRESS,
    )
    phone = models.CharField(max_length=50)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    coverage_zones = models.CharField(max_length=50, blank=True, null=True)
    delivery_services = models.CharField(max_length=150, blank=True, null=True)
    operating_hours = models.IntegerField(blank=True, null=True)
    service_rates = models.IntegerField(blank=True, null=True)
    vehicle_types = models.CharField(max_length=100, blank=True, null=True)
    availability = models.CharField(max_length=50, default='a')
    business_sector = models.CharField(max_length=50, choices=[
        ('Logistics', 'Logistics'),
        ('Insurance', 'Insurance'),
        ('Agriculture', 'Agriculture'),
        ('Manufacturing', 'Manufacturing'),
        ('Trading', 'Trading')
    ], default='a')
    pix = models.ImageField(upload_to='merchant')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)  # Correct reference to Product model
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_number = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()  # Quantity of the product in the cart
    paid = models.BooleanField(default=False)  # Whether the cart has been paid for
    amount = models.CharField(max_length=50)  # You can calculate total amount dynamically if needed
    status = models.CharField(max_length=20, blank=True, null=True)  # Status of the cart (optional)
    order_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    canceled = models.BooleanField(default=False)
    cancellation_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.items.model} ({self.user.username})"  # Display the product's model and the user

    @property
    def total_amount(self):
        # Calculate the total amount (price * quantity)
        return self.price * self.quantity

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField()
    phone = models.CharField(max_length=50)
    pay_code = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=255, null=True, blank=True) 
    additional_info = models.TextField()
    payment_date = models.DateTimeField(auto_now_add=True)
    
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
    
class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    
    class Meta:
        unique_together = ('user', 'product')

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)  # e.g., 0.15 for 15%
    commission_type = models.CharField(max_length=20, default='regular')  # e.g., 'regular' or 'premium'
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_number = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Order(models.Model):
    order_id = models.CharField(max_length=100)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(default=timezone.now)
    order_time = models.DateTimeField(default=timezone.now)
    

