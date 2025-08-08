from django.urls import path
from product import views

urlpatterns = [
    path('<int:pk>/', views.view_specific_category, name='specific-category'),
    path('', views.view_categories, name='category-list'),
]
