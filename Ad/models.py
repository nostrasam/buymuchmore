from django.db import models
from merchant.models import Merchant
from partner.models import Partner
from django.utils.text import slugify
# Create your models here.

class SponsoredProduct(models.Model):
    name = models.CharField(max_length=50, null=True,blank=True)
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE,null=True,blank=True)
    partner = models.ForeignKey(Merchant,on_delete=models.CASCADE,null=True,blank=True)
    model = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,max_length=150)
    description = models.TextField(max_length=300, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_price = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    kilogram = models.FloatField()
    availability = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    front_img = models.ImageField(upload_to='media/images',blank=True, null=True)
    side_img = models.ImageField(upload_to='media/images',blank=True, null=True)
    closeup_img = models.ImageField(upload_to='media/images',blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    
    def save(self, *args, **kwargs):
        slug_name = f"{self.subcategory.name}|-|{self.merchant.company_name}+{self.name}"
        self.subcategory_slug = slugify(slug_name)

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    


class HomePageBannerAd(models.Model):
    brand = models.CharField(max_length=255)
    banner_image = models.ImageField(upload_to='media/ads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    display_time = models.CharField (max_length=255,default='1 day')

    def __str__(self):
        return f"{self.brand}||{self.uploaded_at}"
    



