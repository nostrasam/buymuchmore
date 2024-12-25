from rest_framework import serializers
from .models import *
from product.models import Product

# create serializers here

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('user','company_name','company_email','bio',
                  'address','company_phone_number1','company_phone_number2','postcode','coverage_zones','operating_hours',
                  'service_rates','availability','business_sector',
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
   
    


class MerchantAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','slug','description','subcategory','merchant','model','condition','color','quantity','availability','kilogram',
                  'address','postcode','price','promo_price','front_img','side_img','closeup_img',
                  'is_vat_exempt',)
        read_only_fields = ('merchant','slug',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            merchant = Merchant.objects.get(user=user)
        except:
            raise serializers.ValidationError('Merchant profile does not exist for the current user')

        validated_data['merchant'] = merchant
        return super().create(validated_data)

    def update(self,instance, validated_data):
        user = self.context['request'].user
        try:
            merchant = Merchant.objects.get(user=user)
        except:
            raise serializers.ValidationError('Merchant profile does not exist for the current user')

        validated_data['merchant'] = merchant
        return super().update(instance, validated_data)




class MerchantKYCUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant_KYC_Upload
        fields = ('merchant','tax_document','registration_document',)
        read_only_fields = ('merchant',)

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            merchant = Merchant.objects.get(user=user)
        except:
            raise serializers.ValidationError('Merchant profile does not exist for the current user')

        validated_data['merchant'] = merchant
        return super().create(validated_data)
    


