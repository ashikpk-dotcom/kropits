from django.contrib import admin
from .models import FarmerProduct

@admin.register(FarmerProduct)
class FarmerProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'quantity', 'unit', 'price_per_unit', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'farmer__first_name', 'farmer__last_name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
