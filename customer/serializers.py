from rest_framework import serializers
from .models import Customer

# create serializers here
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user','address','cusstomer_image','security_pin')
        read_only_fields = ('user',)

