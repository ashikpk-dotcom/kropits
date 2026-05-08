from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from farmers.models import FarmerProduct

class BuyerRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('completed', _('Completed')),
    )

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests', verbose_name=_('buyer'))
    product = models.ForeignKey(FarmerProduct, on_delete=models.CASCADE, related_name='requests', verbose_name=_('product'))
    quantity_requested = models.DecimalField(_('quantity requested'), max_digits=10, decimal_places=2)
    unit = models.CharField(_('unit'), max_length=10)
    offered_price = models.DecimalField(_('offered price'), max_digits=10, decimal_places=2)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField(_('delivery address'))
    delivery_location = models.CharField(_('delivery location'), max_length=100, null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Buyer Request')
        verbose_name_plural = _('Buyer Requests')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.buyer.get_full_name()} - {self.product.name}"
