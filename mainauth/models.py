from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)  # Optional username
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  
        editable=False ,
        unique=True 
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,null=False,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class CustomUserVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, unique=True, blank=True, null=True)  # Ensure null handling
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
