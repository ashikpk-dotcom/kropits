from django.urls import path
from .views import BuyerRequestListCreateView, BuyerRequestDetailView, NearbyFarmersView, buyer_dashboard

urlpatterns = [
    path('requests/', BuyerRequestListCreateView.as_view(), name='buyer-request-list-create'),
    path('requests/<int:pk>/', BuyerRequestDetailView.as_view(), name='buyer-request-detail'),
    path('nearby-farmers/', NearbyFarmersView.as_view(), name='nearby-farmers'),
    path('dashboard/', buyer_dashboard, name='buyer-dashboard'),
]
