from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Order, DeliveryPartner, DeliveryAssignment
from buyers.serializers import BuyerRequestSerializer

class OrderSerializer(serializers.ModelSerializer):
    buyer_request_details = BuyerRequestSerializer(source='buyer_request', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer_request', 'buyer_request_details', 'order_number', 'status', 'payment_status', 'total_amount', 'delivery_fee', 'delivery_address', 'delivery_location', 'estimated_delivery', 'actual_delivery', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = DeliveryPartner
        fields = ['id', 'user', 'user_name', 'vehicle_type', 'vehicle_number', 'license_number', 'is_available', 'current_location', 'rating', 'total_deliveries']
        read_only_fields = ['id', 'rating', 'total_deliveries']


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    order_details = OrderSerializer(source='order', read_only=True)
    delivery_partner_name = serializers.CharField(source='delivery_partner.user.get_full_name', read_only=True)

    class Meta:
        model = DeliveryAssignment
        fields = ['id', 'order', 'order_details', 'delivery_partner', 'delivery_partner_name', 'status', 'pickup_location', 'pickup_time', 'delivery_time', 'proof_of_delivery', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProofUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAssignment
        fields = ['proof_of_delivery']
