from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView,Response
import uuid
from product.models import Product
# Create your views here.

class CartView(APIView):
    #
    def get_cart(self, request):
        user = self.request.user

        if user.is_authenticated:
            cart,created = Cart.objects.get_or_create(user=user)

        elif not user.is_authenticated:
            cart_id = request.session.get('cart_id')

            if not cart_id:
                cart_id  = str(uuid.uuid4())
                request.session['cart_id'] = cart_id
            cart,created = Cart.objects.get_or_create(cart_id=cart_id, user=None)

        return cart

    def get(self, request):

        # Get Cart Data For Authenticated Or Anonymous Users
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self,request):
        cart = self.get_cart(request)
        product_slug = request.data.get('product')
        quantity = request.data.get('quantity',1)

        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item, created = CartItems.objects.create(cart=cart,product=product)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    
    def put(self,request,item_id):
        cart = self.get_cart(request)

        try:
            cart_item = CartItems.objects.get(cart=cart, id=item_id)
            serializer = CartItemSerializer(cart_item,data=request.data)
            if serializer.is_valid():
                return Response({'message':'Product quantity has been updated'},status=status.HTTP_200_OK)
            return Response({'message':'Error in updating Product Quantity'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)


    
    def delete(self, request,item_id):
        cart = self.get_cart(request)

        try:
            cart_item = CartItems.objects.get(cart=cart, id=item_id)
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_200_OK)
        except CartItems.DoesNotExist:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

