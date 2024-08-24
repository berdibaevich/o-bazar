import pytest
from orders.models import Order, OrderItem

# TEST ORDER MODEL
@pytest.mark.django_db
def test_order_table(client, get_order):
    new_order = get_order
    order = Order.objects.all()
    assert order.count() == 1
    assert new_order.__str__() == order.first().__str__()
# END TEST ORDER MODEL


# TEST ORDERITEM MODEL
@pytest.mark.django_db
def test_orderitem_table(client, get_orderitem):
    new_orderitem = get_orderitem
    orderitem = OrderItem.objects.all()
    assert new_orderitem.__str__() == orderitem.first().__str__()
# END TEST ORDERITEM MODEL