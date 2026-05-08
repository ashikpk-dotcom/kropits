from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class FarmerProduct(models.Model):
    CATEGORY_CHOICES = (
        ('vegetables', _('Vegetables')),
        ('fruits', _('Fruits')),
        ('grains', _('Grains')),
        ('pulses', _('Pulses')),
        ('spices', _('Spices')),
        ('dairy', _('Dairy')),
    )

    UNIT_CHOICES = (
        ('kg', _('Kilogram')),
        ('quintal', _('Quintal')),
        ('ton', _('Ton')),
        ('piece', _('Piece')),
        ('dozen', _('Dozen')),
    )

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name=_('farmer'))
    name = models.CharField(_('product name'), max_length=100)
    category = models.CharField(_('category'), max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(_('description'), blank=True)
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2)
    unit = models.CharField(_('unit'), max_length=10, choices=UNIT_CHOICES, default='kg')
    price_per_unit = models.DecimalField(_('price per unit'), max_digits=10, decimal_places=2)
    is_available = models.BooleanField(_('available'), default=True)
    harvest_date = models.DateField(_('harvest date'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Farmer Product')
        verbose_name_plural = _('Farmer Products')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.farmer.get_full_name()}"
