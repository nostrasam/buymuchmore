from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import *
from rest_framework.views import Response

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
                                          subcategory__subcategory_slug = self.kwargs['subcategory_slug']
                                          )
        return queryset




class SingleSubcategoryProductDetailView(RetrieveAPIView):
    serializer_class = SingleProductSerializer

    def object(self):
        queryset = Product.objects.filter(subcategory__category__category_slug = self.kwargs['categ_slug'],
                                          subcategory__subcategory_slug = self.kwargs['subcategory_slug'],
                                          slug = self.kwargs['product_slug'])
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = Product.objects.get(slug=self.kwargs['product_slug'])
        product.total_views += 1
        product.save()

        similar_products = instance.get_similar_products
        similar_products_serializer = ViewProductSerializer(similar_products,many=True)

        response_data = serializer.data
        response_data['similar_products'] = similar_products_serializer.data

        return Response(response_data)




class ProductListView(ListAPIView):
    serializer_class = ViewProductSerializer
    queryset = Product.objects.order_by('?')



class SingleProductDetailView(RetrieveAPIView):
    serializer_class = SingleProductSerializer

    def object(self):
        queryset = Product.objects.filter(slug = self.kwargs['product_slug'])
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = Product.objects.get(slug=self.kwargs['product_slug'])
        product.total_views += 1
        product.save()

        similar_products = instance.get_similar_products
        similar_products_serializer = ViewProductSerializer(similar_products,many=True)

        response_data = serializer.data
        response_data['similar_products'] = similar_products_serializer.data

        return Response(response_data)




class ReviewProductView(CreateAPIView):
    serializer_class = ReviewProductSerializer
    queryset = Review.objects.all()




class RatingProductView(CreateAPIView):
    serializer_class = RatingProductSerializer
    queryset = Rating.objects.all()




class NewProductView(ListAPIView):
    serializer_class = ViewProductSerializer

    def get_object(self):
        queryset = Product.objects.filter('-uploaded_at')[20]
        return queryset
    


class DiscountProductsView(ListAPIView):
    serializer_class = ViewProductSerializer

    def get_object(self):
        queryset = Product.objects.filter(discount=True)
        return queryset

    

