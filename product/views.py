from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import *

# Create your views here.

class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()



class SingleCategoryListView(RetrieveAPIView):
    serializer_class = SingleCategorySerializer

    def get_object(self):
        queryset = Category.objects.filter(category_slug=self.kwargs['category_slug'])
        return queryset



class SubcategoryListView(ListAPIView):
    serializer_class = SubcategorySerializer

    def get_object(self):
        queryset = Subcategory.objects.filter(category__category_slug = self.kwargs['categ_slug'])
        return queryset



class SingleSubcategoryListView(RetrieveAPIView):
    serializer_class = SingleSubCategorySerializer

    def get_object(self):
        queryset = Subcategory.objects.filter(category__category_slug = self.kwargs['categ_slug'], subcategory_slug = self.kwargs['subcategory_slug'])
        return queryset
    


class SingleSubcategoryProductListView(ListAPIView):
    serializer_class = ViewProductSerializer

    def get_object(self):
        queryset = Product.objects.filter(subcategory__category__category_slug = self.kwargs['categ_slug'],
                                          subcategory__subcategory_slug = self.kwargs['subcategory_slug'])
        
        return queryset


class SingleSubcategoryProductDetailView(RetrieveAPIView):
    serializer_class = SingleProductSerializer

    def object(self):
        queryset = Product.objects.filter(subcategory__category__category_slug = self.kwargs['categ_slug'],
                                          subcategory__subcategory_slug = self.kwargs['subcategory_slug'],
                                          slug = self.kwargs['product_slug'])
        return queryset


class ReviewProductView(CreateAPIView):
    serializer_class = ReviewProductSerializer
    queryset = Review.objects.all()


class RatingProductView(CreateAPIView):
    serializer_class = RatingProductSerializer
    queryset = Rating.objects.all()