import pytest
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from rest_framework import status

from orders.models import (
    Order,
    OrderItem
)

from api.serializers import (
    OrderDetailSerializers,
    OrderItemDetailSerializers,
    OrderItemListSerializers,
    OrderListSerializers
)




# TEST ORDERS LIST API VIEW GET
@pytest.mark.django_db
def test_orders_api_view_get(api_client, get_customer_login, get_customer, get_order):
    customer = get_customer
    url = reverse("api:orders", kwargs={"id": customer.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    orders = get_list_or_404(Order.objects.select_related("user"), user__id = customer.id)
    serializer = OrderListSerializers(orders, many = True, context = {"request": response.wsgi_request})
    expected_response = {
        "orders": serializer.data,
        "num_of_orders": len(orders)
    }
    assert response.data == expected_response
# END TEST ORDERS LIST API VIEW GET


# TEST ORDER DETAIL API VIEW GET
@pytest.mark.django_db
def test_order_api_view_get(api_client, get_customer_login, get_order):
    order = get_order
    url = reverse("api:order-detail", kwargs={"id": order.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    order = get_object_or_404(Order.objects.select_related("address", "user"), id = order.id)
    serializer = OrderDetailSerializers(order, many = False, context = {"request":response.wsgi_request})
    expected_response = {
        "order_detail": serializer.data
    }
    assert response.data == expected_response
# ENDTEST ORDER DETAIL API VIEW GET



# TEST ORDER ITEMS LIST API VIEW GET
@pytest.mark.django_db
def test_orderitems_api_view_get(api_client, get_customer_login, get_order, get_orderitem):
    order = get_order
    url = reverse("api:order-items", kwargs={"id": order.id})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK

    orderitems = get_list_or_404(OrderItem.objects.select_related("order", "product__product"), order__id = order.id)
    serializer = OrderItemListSerializers(orderitems, many = True, context = {"request": response.wsgi_request})
    expected_response = {
        "items": serializer.data,
        "num_of_items": len(orderitems)
    }
    assert response.data == expected_response
# END TEST ORDER ITEMS LIST API VIEW GET


# TEST ORDER ITEM DETAIL API VIEW GET
@pytest.mark.django_db
def test_orderitem_api_view_get(api_client, get_customer_login, get_orderitem):
    orderitem = get_orderitem
    url = reverse("api:item-detail", kwargs={"id": orderitem.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    orderitem = get_object_or_404(OrderItem.objects.select_related("order", "product__product"), id = orderitem.id)
    serializer = OrderItemDetailSerializers(orderitem, many = False)
    expected_response = {
        "item_detail": serializer.data
    }
    assert response.data == expected_response
# END TEST ORDER ITEM DETAIL API VIEW GET