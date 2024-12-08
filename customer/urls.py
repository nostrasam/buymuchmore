from django.urls import path
from .views import *


urlpatterns = [
    path('customer-profile',CustomerProfileView.as_view(),name='customer_profile')
]