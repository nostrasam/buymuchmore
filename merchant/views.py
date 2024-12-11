from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import *
from product.models import Product

# Create your views here.

class MerchantCreationView(CreateAPIView):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()




class MerchantAddProductView(CreateAPIView):
    serializer_class = MerchantAdminSerializer
    queryset = Product.objects.all()




class MerchantViewUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = MerchantAdminSerializer
    queryset = Product.objects.all()




class MerchantKYCUploadView(CreateAPIView):
    serializer_class = MerchantKYCUploadSerializer
    queryset = Merchant_KYC_Upload.objects.all()