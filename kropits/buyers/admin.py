from django.contrib import admin
from .models import BuyerRequest

@admin.register(BuyerRequest)
class BuyerRequestAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'quantity_requested', 'unit', 'offered_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__first_name', 'buyer__last_name', 'product__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
