from django.urls import path
from product import views

urlpatterns = [
    path('<int:pk>/', views.view_specific_product, name='specific-product'),
    path('', views.view_products, name='product-list'),
]
