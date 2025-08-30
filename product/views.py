from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .filters import ProductFilter
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions
from .paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermission
from .permissions import IsReviewAuthorOrReadOnly

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [FullDjangoModelPermission]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({'message': "Product stock more than 10 could not be deleted"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
