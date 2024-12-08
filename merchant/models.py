from django.db import models
from mainauth.models import CustomUser
# Create your models here.

class Merchant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    company_registration = models.CharField(max_length=50, blank=True, null=True)
    company_email = models.EmailField(max_length=254)
    bio = models.TextField()
    address = models.CharField(max_length=150)
    company_phone_number = models.CharField(max_length=50)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    coverage_zones = models.CharField(max_length=50, blank=True, null=True)
    operating_hours = models.IntegerField(blank=True, null=True)
    service_rates = models.IntegerField(blank=True, null=True)
    vehicle_types = models.CharField(max_length=100, blank=True, null=True)
    availability = models.CharField(max_length=50, choices=[
        ('Available', 'Available'),
        ('Not Available', 'Not Available')
    ], default='Available')
    business_sector = models.CharField(max_length=50, choices=[
        ('Logistics', 'Logistics'),
        ('Insurance', 'Insurance'),
        ('Agriculture', 'Agriculture'),
        ('Manufacturing', 'Manufacturing'),
        ('Trading', 'Trading')
    ],)
    logo = models.ImageField(upload_to='merchant')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    
    
    def __str__(self):
        return self.user.username