from celery import shared_task
from django.utils import timezone
from logistics.models import Order, DeliveryAssignment, DeliveryPartner
from buyers.models import BuyerRequest
from .matching import match_farmer_to_buyer, predict_demand
from .routing import optimize_delivery_routes
from django.utils.translation import gettext_lazy as _

@shared_task
def optimize_routes_task():
    pending_orders = Order.objects.filter(
        status='confirmed',
        delivery_assignment__isnull=True
    )

    deliveries = []
    for order in pending_orders:
        deliveries.append({
            'order_id': order.id,
            'location': (0, 0),
        })

    if deliveries:
        routes = optimize_delivery_routes(deliveries)
        return {'status': 'success', 'routes': routes}
    return {'status': 'no deliveries to optimize'}


@shared_task
def predict_demand_task(category, lat, lon):
    prediction = predict_demand(category, (lon, lat))
    return prediction


@shared_task
def auto_assign_delivery_task():
    pending_orders = Order.objects.filter(
        status='confirmed',
        delivery_assignment__isnull=True
    )

    assigned = 0
    for order in pending_orders:
        available_partners = DeliveryPartner.objects.filter(
            is_available=True
        )[:1]

        if available_partners:
            partner = available_partners[0]
            DeliveryAssignment.objects.create(
                order=order,
                delivery_partner=partner,
                pickup_location=order.buyer_request.product.farmer.location,
            )
            order.status = 'assigned'
            order.save()
            partner.is_available = False
            partner.save()
            assigned += 1

    return {'assigned': assigned}
