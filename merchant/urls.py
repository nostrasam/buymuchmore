from django.urls import path
from .views import *

urlpatterns = [
    path('merchant-creation/',MerchantCreationView.as_view(),name='merchant_creation')

]