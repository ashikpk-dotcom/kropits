from farmers.models import FarmerProduct
from buyers.models import BuyerRequest
from django.utils.translation import gettext_lazy as _
import numpy as np

def match_farmer_to_buyer(buyer_request):
    product = buyer_request.product
    quantity_needed = buyer_request.quantity_requested

    available_products = FarmerProduct.objects.filter(
        is_available=True,
        category=product.category,
        quantity__gte=quantity_needed,
    ).order_by('price_per_unit')[:10]

    matches = []
    for farmer_product in available_products:
        score = calculate_match_score(farmer_product, buyer_request)
        matches.append({
            'farmer_product_id': farmer_product.id,
            'farmer_name': farmer_product.farmer.get_full_name(),
            'product_name': farmer_product.name,
            'distance_km': 0,
            'price_per_unit': float(farmer_product.price_per_unit),
            'quantity_available': float(farmer_product.quantity),
            'match_score': score,
        })

    return sorted(matches, key=lambda x: x['match_score'], reverse=True)


def calculate_match_score(farmer_product, buyer_request):
    score = 100

    if farmer_product.price_per_unit <= buyer_request.offered_price:
        score += 20
    else:
        score -= 10

    if farmer_product.harvest_date and farmer_product.harvest_date >= buyer_request.created_at.date():
        score += 15

    return min(max(score, 0), 100)


def predict_demand(product_category, location, days_ahead=7):
    from django.db.models import Sum
    from datetime import timedelta
    from django.utils import timezone

    past_date = timezone.now() - timedelta(days=30)
    past_requests = BuyerRequest.objects.filter(
        product__category=product_category,
        created_at__gte=past_date,
    )

    total_quantity = past_requests.aggregate(Sum('quantity_requested'))['quantity_requested__sum'] or 0
    avg_daily = total_quantity / 30 if total_quantity > 0 else 0

    predicted = avg_daily * days_ahead

    return {
        'category': product_category,
        'predicted_quantity': predicted,
        'confidence': 0.7 if total_quantity > 0 else 0.3,
    }
