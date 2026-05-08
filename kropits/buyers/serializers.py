from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import BuyerRequest
from farmers.serializers import FarmerProductSerializer

class BuyerRequestSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    product_details = FarmerProductSerializer(source='product', read_only=True)

    class Meta:
        model = BuyerRequest
        fields = ['id', 'buyer', 'buyer_name', 'product', 'product_details', 'quantity_requested', 'unit', 'offered_price', 'status', 'delivery_address', 'delivery_location', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'buyer', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)


class NearbyFarmerSerializer(serializers.Serializer):
    farmer_id = serializers.IntegerField()
    farmer_name = serializers.CharField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    distance = serializers.FloatField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
