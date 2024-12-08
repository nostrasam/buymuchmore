from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import *

# Create your views here.

class CustomerProfileView(RetrieveUpdateDestroyAPIView):   
    serializer_class = CustomerProfileSerializer
    queryset = Customer.objects.all()

    def get_object(self):
        customer = Customer.objects.get(user = self.request.user)
        return customer  # Assuming each customer has a user profile associated with them

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()