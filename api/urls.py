from django.urls import path, include
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)

prouduct_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
prouduct_router.register('reviews', ReviewViewSet, basename='product-review')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(prouduct_router.urls)),
]