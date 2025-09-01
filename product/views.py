from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from .filters import ProductFilter
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from .permissions import IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store.
    - Allows authenticated Admin to Create, Update & Delete Products.
    - Allows Users to brows and filter Products.
    """
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product stock more than 10 could not be deleted"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
            operation_summary="Retrieve a list of Products"
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the Products"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary="Create a Product by Admin.",
            operation_description="This allow an Admin to create a Product.",
            request_body=ProductSerializer,
            responses={
                201: ProductSerializer,
                400: "Bad Request"
            }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated Admin can create Product"""
        return super().create(request, *args, **kwargs)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
