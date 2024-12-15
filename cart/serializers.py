from rest_framework import serializers
from .models import *
from product.serializers import CartProductSerializer

# create serializers here
class CartItemSerializer(serializers.ModelSerializer):
    product_cartitem = CartProductSerializer(many=False)
    class Meta:
        model = CartItems
        fields = ('id','cart','product_cartitem','price','quantity','subtotal_price',)
        read_only_fields = ('cart',)


class CartSerializer(serializers.ModelSerializer):
    cart_cartitems = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ('cart_id','user','total_amount','status',)
        read_only_fields = ('cart_id','user','status',)

    # Calculate the total sum of products
        def get_total_amount(self,obj):
            item = obj.cart_items.all()
            return sum(item.quantity * item.product.price)