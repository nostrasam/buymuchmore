from django.db import models
from mainauth.models import CustomUser
from merchant.models import Merchant
from django.utils.text import slugify
from customer.models import Customer

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    category_slug = models.SlugField(max_length=20, unique=True, null=True)
    description = models.CharField(max_length=100,null=True, blank=True)
    category_img = models.ImageField(upload_to='media/images')

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
    description = models.CharField(max_length=100,null=True, blank=True)
    subcategory_img = models.ImageField(upload_to='media/images')

    def save(self, *args, **kwargs):
        slug_name = f"{self.category.name}--{self.name}"
        self.subcategory_slug = slugify(slug_name)

        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.name}'



class Product(models.Model):
    name = models.CharField(max_length=50, null=True,blank=True)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE, related_name='subcateg_products')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE,related_name='product_merchant') 
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
        return self.model
    



class Rating(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='rating_customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='rating_product')
    rating = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('product','customer') # Ensure one immutable review per customer

    def __str__(self):
        return f"{self.customer}||{self.product}||{self.rating}"



class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('product','customer') # Ensure one immutable review per customer

    def __str__(self):
        return f"{self.customer}||{self.product}||{self.review_text[:10]}"
    