from django.contrib import admin
from .models import Order, DeliveryPartner, DeliveryAssignment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'buyer_request', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'buyer_request__buyer__first_name', 'buyer_request__product__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'vehicle_number', 'is_available', 'rating', 'total_deliveries')
    list_filter = ('is_available', 'vehicle_type')
    search_fields = ('user__first_name', 'user__last_name', 'vehicle_number', 'license_number')


@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_partner', 'status', 'pickup_time', 'delivery_time', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'delivery_partner__user__first_name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
