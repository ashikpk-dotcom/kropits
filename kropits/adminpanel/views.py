from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from farmers.models import FarmerProduct
from buyers.models import BuyerRequest
from logistics.models import Order, DeliveryPartner

def is_admin(user):
    return user.role == 'admin' or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_farmers': User.objects.filter(role='farmer').count(),
        'total_buyers': User.objects.filter(role='buyer').count(),
        'total_products': FarmerProduct.objects.filter(is_available=True).count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'total_delivery_partners': DeliveryPartner.objects.count(),
        'available_partners': DeliveryPartner.objects.filter(is_available=True).count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def verify_farmers(request):
    farmers = User.objects.filter(role='farmer')
    return render(request, 'adminpanel/verify_farmers.html', {'farmers': farmers})


@login_required
@user_passes_test(is_admin)
def orders_overview(request):
    orders = Order.objects.all().select_related('buyer_request__buyer', 'buyer_request__product__farmer')
    return render(request, 'adminpanel/orders_overview.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def pricing_insights(request):
    products = FarmerProduct.objects.filter(is_available=True).order_by('price_per_unit')
    return render(request, 'adminpanel/pricing_insights.html', {'products': products})
