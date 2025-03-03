from django.contrib import admin
from main.models import *
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils.timezone import now

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}
    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('model',)}
    list_display = ['id', 'type', 'model', 'price', 'description', 'telephone1', 'telephone2', 'seller_name', 'uploaded_at', 'updated_at', 'ingredients', 'instructions']
    

class FeatureItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}
    
class SubscriptionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand',)}   
    
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'items', 'amount']
    
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'ingredients', 'instruction']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'user', 'amount', 
        'paid', 'pay_code', 'payment_date', 'invoice_number', 'related_orders'
    ]
    list_filter = ['payment_date', 'paid']  # Filter by date and payment status
    search_fields = ['pay_code', 'user__username', 'invoice_number']

    def related_orders(self, obj):
        """Display related orders for each payment."""
        orders = obj.orders.all()
        return ", ".join(order.order_id for order in orders)

    def get_queryset(self, request):
        """Annotate total order amounts for admin view."""
        qs = super().get_queryset(request)
        return qs.annotate(total_amount=Sum('orders__payment__amount'))

    actions = ['filter_daily', 'filter_weekly', 'filter_monthly']

    def filter_daily(self, request, queryset):
        """Filter payments made today."""
        today = now().date()
        filtered_queryset = queryset.filter(payment_date__date=today)
        self.message_user(request, f"Filtered {filtered_queryset.count()} payments made today.")
        return filtered_queryset

    filter_daily.short_description = "Filter Payments - Daily"

    def filter_weekly(self, request, queryset):
        """Filter payments made in the past 7 days."""
        week_start = now().date() - timedelta(days=7)
        filtered_queryset = queryset.filter(payment_date__date__gte=week_start)
        self.message_user(request, f"Filtered {filtered_queryset.count()} payments made this week.")
        return filtered_queryset

    filter_weekly.short_description = "Filter Payments - Weekly"

    def filter_monthly(self, request, queryset):
        """Filter payments made this month."""
        month_start = now().replace(day=1).date()
        filtered_queryset = queryset.filter(payment_date__date__gte=month_start)
        self.message_user(request, f"Filtered {filtered_queryset.count()} payments made this month.")
        return filtered_queryset

    filter_monthly.short_description = "Filter Payments - Monthly"

    
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
admin.site.register(Order)




