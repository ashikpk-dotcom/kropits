from django.urls import path
from .views import admin_dashboard, verify_farmers, orders_overview, pricing_insights

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
    path('verify-farmers/', verify_farmers, name='verify-farmers'),
    path('orders-overview/', orders_overview, name='orders-overview'),
    path('pricing-insights/', pricing_insights, name='pricing-insights'),
]
