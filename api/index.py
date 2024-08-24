from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from inventory.models import (
    ProductInventory,
    Product
)

@register(ProductInventory)
class ProductInventoryIndex(AlgoliaIndex):
    fields = [
        'product',
        'brand',
        'sale_price'
    ]



@register(Product)
class ProductIndex(AlgoliaIndex):
    fields = [
        "name",
        "description",
        "category"
    ]

