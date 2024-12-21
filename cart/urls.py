from django.urls import path
from .views import *

urlpatterns = [
    # View and manage the cart (GET, POST)
    path('cart/', CartView.as_view(), name='cart'),
    
    # Delete and update an item from the cart
    path('cart/<int:item_id>/', CartView.as_view(), name='cart-item-delete'),
]