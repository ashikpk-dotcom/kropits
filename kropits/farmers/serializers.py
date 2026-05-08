from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import FarmerProduct

class FarmerProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)

    class Meta:
        model = FarmerProduct
        fields = ['id', 'farmer', 'farmer_name', 'name', 'category', 'description', 'quantity', 'unit', 'price_per_unit', 'is_available', 'harvest_date', 'location', 'created_at', 'updated_at']
        read_only_fields = ['id', 'farmer', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['farmer'] = self.context['request'].user
        return super().create(validated_data)
