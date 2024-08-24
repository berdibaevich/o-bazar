from django.db import models
from decimal import Decimal
from django.conf import settings

from inventory.models import ProductInventory
from account.models import Address

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="user_address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=15, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.created_at)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInventory, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


    