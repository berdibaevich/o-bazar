from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Delivery(models.Model):
    """
    The Delivery Table
    """
    DELIVERY_CHOICES = [
        ('IS', 'In Store'),
        ('HD', 'Home Delivery'),
        ('DD', 'Digital Delivery'),
    ]

    delivery_name = models.CharField(verbose_name=_("delivery name"), help_text=_("required"), max_length=255)
    delivery_price = models.DecimalField(
        verbose_name=_("Delivery price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name":{
                "max_length": _("The price must be between 0 and 999.99")
            }
        },
        max_digits=5,
        decimal_places=2
    )

    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("delivery_method"),
        help_text=_("Required"),
        max_length=255,
    )

    #delivery_timeframe means when your product will be your hand like that
    delivery_timeframe = models.CharField(
        verbose_name=_("delivery timeframe"),
        help_text=_("Required"),
        max_length=255,
    )

    delivery_window = models.CharField(
        verbose_name=_("delivery window"),
        help_text=_("Required"),
        max_length=255,
    )

    order = models.IntegerField(
        verbose_name=_("List Order"),
        help_text=_("Required"),
        default=0
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    
    def __str__(self):
        return self.delivery_name


