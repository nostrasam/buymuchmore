from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import *
from product.models import Product

# Create your views here.

class PartnerCreationView(CreateAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()



class PartnerKYCUploadView(CreateAPIView):
    serializer_class = PartnerKYCUploadSerializer
    queryset = Partner_KYC_Upload.objects.all()