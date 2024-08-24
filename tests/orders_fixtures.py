import pytest
from orders.models import Order, OrderItem

# ORDER TABLE FIXTURES
@pytest.fixture
def get_order(db, get_customer, get_address):
    customer = get_customer
    address = get_address
    return Order.objects.create(
        user = customer,
        address = address,
        total_paid = 34.88,
        order_key = "has23616273"
    )
# END ORDER TABLE FIXTURES


# ORDER ITEM TABLE FIXTURES
@pytest.fixture
def get_orderitem(db, get_order, get_productinventory_for_programming):
    order = get_order
    product_inventory = get_productinventory_for_programming
    return OrderItem.objects.create(
        order = order,
        product = product_inventory,
        price = product_inventory.sale_price,
        quantity = 2
    )
# END ORDER ITEM TABLE FIXTURES



# GET ORDER FIXTURES BILLING STATUS TRUE
@pytest.fixture
def get_order_billing_true(db, get_customer, get_address):
    customer = get_customer
    address = get_address
    return Order.objects.create(
        user = customer,
        address = address,
        total_paid = 34.88,
        order_key = "has23616273",
        billing_status = True
    )
# END GET ORDER FIXTURES BILLING TRUE



# GET ORDERITEMS ORDER TABLE BILLING STATUS TRUE
@pytest.fixture
def get_orderitem_bst(db, get_order_billing_true, get_productinventory_for_programming):
    order = get_order_billing_true
    product_inventory = get_productinventory_for_programming
    return OrderItem.objects.create(
        order = order,
        product = product_inventory,
        price = product_inventory.sale_price,
        quantity = 2
    )
# END GET ORDERITEMS ORDER TABLE BILLING STATUS TRUE