from inventory.models import ProductInventory
from decimal import Decimal

# TEST PRODUCTINVENTORY TABLE


# TEST CREATE PRODUCTINVENTORY
def test_create_productinventory(get_productinventory):
    new_productinventory = get_productinventory
    productinventory = ProductInventory.objects.first()
    assert productinventory.id == new_productinventory.id
    assert productinventory.product.name == new_productinventory.product.name
    assert productinventory.upc == new_productinventory.upc
# END TEST CREATE PRODUCTINVENTORY









# END TEST PRODUCTINVENTORY TABLE