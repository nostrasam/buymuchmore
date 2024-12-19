from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from mainauth.models import CustomUser
from geopy.geocoders import Nominatim

# Create your models here.

geolocator = Nominatim(user_agent='location')

class Merchant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    company_email = models.EmailField(max_length=254)
    company_phone_number1 = models.CharField(max_length=50)
    company_phone_number2 = models.CharField(max_length=50,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    coverage_zones = models.CharField(max_length=50, blank=True, null=True)
    operating_hours = models.IntegerField(blank=True, null=True)
    service_rates = models.IntegerField(blank=True, null=True)
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
    company_registration_kyc = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='merchant')
    location = models.PointField(geography=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        g = geolocator.geocode(self.address)
        lat = g.latitude
        lng = g.longitude
        self.location = Point(lng,lat)
        
        super().save(*args,**kwargs)


    def __str__(self):
        return f"{self.company_name}||{self.company_email}"
    

class Merchant_KYC_Upload(models.Model):
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE)
    tax_document = models.ImageField(upload_to='media/images')
    registration_document = models.ImageField(upload_to='media/images')
    
    def __str__(self):
        return f'{self.merchant.company_name}||{self.merchant.company_email}'



