from django.urls import path
from .views import *

urlpatterns = [
    path('merchant-creation/',MerchantCreationView.as_view(),name='merchant_creation'),
    path('merchant-admin-addproducts/',MerchantAddProductView.as_view(),name='merchant_addproducts'),
    path('merchant-admin/',MerchantViewUpdateDeleteView.as_view(),name='merchant_admin'),
    path('merchant-kyc-upload/', MerchantKYCUploadView.as_view(),name='merchant_kyc_upload'),
]