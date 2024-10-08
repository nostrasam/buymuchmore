from django.contrib import admin
from main.models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}
    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('model',)}
    list_display = ['id', 'type', 'model', 'price', 'description', 'telephone1', 'telephone2', 'seller_name', 'uploaded_at', 'updated_at']
    

class FeatureItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}
    
class SubscriptionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}   
    
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'items', 'amount']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'amount', 'paid', 'pay_code', 'payment_date']
    
class SubscribeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('plan',)}
    list_display = ['id', 'plan', 'description', 'price', 'promo_price']
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'address', 'address_type', 'postcode', 'coverage_zones', 'operating_hours', 'service_rates', 'availability', 'business_sector']
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'address', 'phone', 'email', 'user']
    

admin.site.register(AppInfo)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FeatureItem, FeatureItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Subscribe, SubscribeAdmin)



