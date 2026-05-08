from django.urls import path
from .views import ProductListCreateView, ProductDetailView, AvailabilityToggleView, farmer_dashboard, add_product

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('availability/<int:pk>/', AvailabilityToggleView.as_view(), name='availability-toggle'),
    path('dashboard/', farmer_dashboard, name='farmer-dashboard'),
    path('add-product/', add_product, name='add-product'),
]
