from rest_framework import serializers
from .models import *

# create serializers here

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('user','company_name','company_registration','company_email','bio',
                  'address','company_phone_number','postcode','coverage_zones','operating_hours',
                  'service_rates','vehicle_types','availability','business_sector',
                  'logo',
                  )
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        if not CustomUser.objects.filter(email=user.email, is_active=True).exists():     
            raise serializers.ValidationError('User is not Registered')
        
    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['user'] = user
        return super().create(validated_data)


