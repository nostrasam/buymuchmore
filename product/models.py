from django.db import models
from mainauth.models import CustomUser
from merchant.models import Merchant
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    category_slug = models.SlugField(max_length=20, unique=True, null=True)

    def save(self, *args, **kwargs):
        slug_name = f"++{self.name}++"
        self.category_slug = slugify(slug_name)

        super().save(*args,**kwargs)


    def __str__(self):
        return f'{self.name}'



class Subcategory(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categ_subcategory')
    subcategory_slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        slug_name = f"{self.category.name}--{self.name}"
        self.subcategory_slug = slugify(slug_name)

        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller_name = models.ForeignKey(Merchant, on_delete=models.CASCADE) 
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
    message = models.TextField(blank=True, null=True)
    carimg = models.ImageField(upload_to='carimg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating_value = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    is_vat_exempt = models.BooleanField(default=False, help_text="Select if this product is VAT exempt (0%).")
    total_views = models.PositiveIntegerField(default=0)  # Total views for the product
    total_customers = models.PositiveIntegerField(default=1)  # Total unique customers for the product, default is 1 to avoid division by zero
    
    

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