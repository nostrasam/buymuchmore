from django.db import models
from mainauth.models import CustomUser
# Create your models here.
  
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    customer_picture = models.ImageField(upload_to='media/images',blank=True, null=True)
    
    
    def __str__(self):
        return self.user.email