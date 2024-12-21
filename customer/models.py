from django.db import models
from mainauth.models import CustomUser
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

# Create your models here.

geolocator = Nominatim(user_agent="location")
  
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    customer_picture = models.ImageField(upload_to='media/images',blank=True, null=True)
    location = models.PointField(geography=True,null=True,blank=True)
    security_pin = models.CharField(max_length=4,null=True,blank=True)

    def save(self, *args, **kwargs):
        g = geolocator.geocode(self.address)
        lat = g.latitude
        lng = g.longitude
        self.location = Point(lng,lat)
        
        super().save(*args,**kwargs)
    
    
    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name}||{self.user.email}"