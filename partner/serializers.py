from rest_framework import serializers
from .models import *
from product.models import Product

# create serializers here

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ('user','partner_name','partner_email',
                  'address','partner_phone_number1','partner_phone_number2','postcode','coverage_zones','operating_hours',
                  'service_rates','availability','business_sector',
                  'logo','location',
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
   
    

class PartnerKYCUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner_KYC_Upload
        fields = ('partner','tax_document','registration_document',)
        read_only_fields = ('partner',)

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            partner = Partner.objects.get(user=user)
        except:
            raise serializers.ValidationError('Partner profile does not exist for the current user')

        validated_data['partner'] = partner
        return super().create(validated_data)
    


