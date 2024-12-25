from django.urls import path
from .views import *

urlpatterns = [
    path('',CategoryListView.as_view(),name='category_list'),
    path('category/',SingleCategoryListView.as_view(),name='category_detail'),
    path('category/subcategory/',SubcategoryListView.as_view(),name='subcategory_list'),
    path('category/subcategory/<str:subcategory_slug>/',SingleSubcategoryProductListView.as_view(),name='subcategory_detail'),
    path('category/subcategory/<str:subcategory_slug>/<str:product_slug>/',SingleSubcategoryProductDetailView.as_view(),name='subcategory_product_detail'),

    path('products/',ProductListView.as_view(),name='product_list'),
    path('products/<str:product_slug>/',SingleProductDetailView.as_view(),name='product_detail'),

    path('new-products/',NewProductView.as_view(),name='new_products'),
    path('discount-products/', DiscountProductsView.as_view(),name='discount_products')
    
    
]