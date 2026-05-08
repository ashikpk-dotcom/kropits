from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from buyers.models import BuyerRequest

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('assigned', _('Assigned to Delivery')),
        ('in_transit', _('In Transit')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', _('Payment Pending')),
        ('completed', _('Payment Completed')),
        ('failed', _('Payment Failed')),
    )

    buyer_request = models.OneToOneField(BuyerRequest, on_delete=models.CASCADE, related_name='order', verbose_name=_('buyer request'))
    order_number = models.CharField(_('order number'), max_length=20, unique=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(_('payment status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(_('total amount'), max_digits=12, decimal_places=2)
    delivery_fee = models.DecimalField(_('delivery fee'), max_digits=10, decimal_places=2, default=0)
    delivery_address = models.TextField(_('delivery address'))
    delivery_location = models.CharField(_('delivery location'), max_length=100, null=True, blank=True)
    estimated_delivery = models.DateTimeField(_('estimated delivery'), null=True, blank=True)
    actual_delivery = models.DateTimeField(_('actual delivery'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class DeliveryPartner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_profile', verbose_name=_('user'))
    vehicle_type = models.CharField(_('vehicle type'), max_length=50)
    vehicle_number = models.CharField(_('vehicle number'), max_length=20)
    license_number = models.CharField(_('license number'), max_length=30)
    is_available = models.BooleanField(_('available'), default=True)
    current_location = models.CharField(_('current location'), max_length=100, null=True, blank=True)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=2, default=0)
    total_deliveries = models.IntegerField(_('total deliveries'), default=0)

    class Meta:
        verbose_name = _('Delivery Partner')
        verbose_name_plural = _('Delivery Partners')

    def __str__(self):
        return self.user.get_full_name()


class DeliveryAssignment(models.Model):
    STATUS_CHOICES = (
        ('assigned', _('Assigned')),
        ('picked_up', _('Picked Up')),
        ('in_transit', _('In Transit')),
        ('delivered', _('Delivered')),
        ('failed', _('Delivery Failed')),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_assignment', verbose_name=_('order'))
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.CASCADE, related_name='assignments', verbose_name=_('delivery partner'))
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='assigned')
    pickup_location = models.CharField(_('pickup location'), max_length=100, null=True, blank=True)
    pickup_time = models.DateTimeField(_('pickup time'), null=True, blank=True)
    delivery_time = models.DateTimeField(_('delivery time'), null=True, blank=True)
    proof_of_delivery = models.ImageField(_('proof of delivery'), upload_to='delivery_proofs/', null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Delivery Assignment')
        verbose_name_plural = _('Delivery Assignments')

    def __str__(self):
        return f"{self.order.order_number} - {self.delivery_partner.user.get_full_name()}"
