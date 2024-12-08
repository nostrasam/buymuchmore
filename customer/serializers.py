from rest_framework import serializers
from .models import Customer

# create serializers here
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('address','pix',)

