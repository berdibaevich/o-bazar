import pytest
from django.urls import reverse


# TEST USER'S ORDERS VIEW GET BUT NO ORDERS YET HAHAHA
@pytest.mark.django_db
def test_user_orders_view_get(client, get_customer, get_order):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    url = reverse("orders:order-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "No orders yet...".encode() in response.content
# END TEST USER'S ORDERS VIEW GET



# TEST USER'S ORDERS VIEW GET ORDERS HAS BILLING STATUS TRUE
@pytest.mark.django_db
def test_user_orders_view_get_bst(client, get_customer, get_order_billing_true, get_orderitem_bst):
    customer = get_customer
    client.login(username = customer.email, password = 'qwerty')
    url = reverse("orders:order-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['orders']) == 1
    assert "Dispacted to".encode() in response.content
# END TEST USER'S ORDERS VIEW GET ORDERS HAS BILLING STATUS TRUE