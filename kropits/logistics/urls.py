from django.urls import path
from .views import OrderCreateView, OrderStatusView, AvailableDeliveryPartnersView, DeliveryAssignView, ProofUploadView, orders_dashboard

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/status/', OrderStatusView.as_view(), name='order-status'),
    path('partners/available/', AvailableDeliveryPartnersView.as_view(), name='available-partners'),
    path('assign/', DeliveryAssignView.as_view(), name='delivery-assign'),
    path('proof-upload/<int:pk>/', ProofUploadView.as_view(), name='proof-upload'),
    path('dashboard/', orders_dashboard, name='orders-dashboard'),
]
