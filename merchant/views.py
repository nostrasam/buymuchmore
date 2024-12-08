from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import *

# Create your views here.

class MerchantCreationView(CreateAPIView):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
