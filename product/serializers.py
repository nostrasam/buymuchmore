from rest_framework import serializers
from .models import *
from merchant.models import Merchant
from customer.models import Customer

# create serializers here
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','category_slug','description','category_img',)
        read_only_fields = ('category_slug',)




class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'category.name', read_only = True)
    class Meta:
        model = Subcategory
        fields = ('name', 'category_name', 'subcategory_slug','description','subcategory_img',)




class ViewProductSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source = 'merchant.company_name', read_only = True)
    class Meta:
        model = Product
        fields = ('name','product_slug','description','subcategory','merchant_name',
                  'address','postcode','price','promo_price','front_img',
                  'is_vat_exempt',)
        read_only_fields = ()




class SingleSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'category.name', read_only = True)
    subcateg_products = ViewProductSerializer(many=True)
    class Meta:
        model = Subcategory
        fields = ('name', 'category_name', 'subcategory_slug','description', 'subcateg_products')
        read_only = ('category_name' , 'subcategory_slug',)

        


class SingleCategorySerializer(serializers.ModelSerializer):
    categ_subcategory = SingleSubCategorySerializer(many = True)
    class Meta:
        model = Category
        fields = ('name','category_slug','categ_subcategory',)



class CartProductSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source = 'merchant.company_name', read_only = True)
    class Meta:
        model = Product
        fields = ('name','product_slug','subcategory','merchant_name',
                  'address','price','promo_price','front_img',
                  'is_vat_exempt',)
        read_only_fields = ()


class ReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('customer','product','review_text','created_at',)
        read_only_fields = ('customer','product',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            customer = Customer.objects.get(user=user)
        except:
            raise serializers.ValidationError('User does not have a customer profile')
        
        product = Product.objects.get(slug=self.kwargs['product_slug'])

        validated_data['customer'] = customer
        validated_data['product'] = product
        return super().create(validated_data)
    

class RatingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('customer','product','rating','created_at',)
        read_only_fields = ('customer','product',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            customer = Customer.objects.get(user=user)
        except:
            raise serializers.ValidationError('User does not have a customer profile')
        
        product = Product.objects.get(slug=self.kwargs['product_slug'])

        validated_data['customer'] = customer
        validated_data['product'] = product
        return super().create(validated_data) 



class SingleProductSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source = 'vendor.brand_name', read_only = True)
    rating_product = RatingProductSerializer(many=True)
    review_product = ReviewProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name','product_slug','description','subcategory','merchant_name','model','condition','color','quantity','availability','kilogram',
                  'address','postcode','price','promo_price','front_img','side_img','closeup_img',
                  'is_vat_exempt','total_views','total_customers','rating_product','review_product',)
        read_only_fields = ('slug','subcategory',)

    

