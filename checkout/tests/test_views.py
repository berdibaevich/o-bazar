import pytest
from django.urls import reverse


# TEST DELIVERY CHOICES VIEWS GET
@pytest.mark.django_db
def test_delivery_choices_view_get(client, get_deliveries, get_customer):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    url = reverse("checkout:deliverychoices")
    response = client.get(url)
    response.status_code == 200
    assert "Delivery Options".encode() in response.content
# TEST DELIVERY CHOICES



# WE HAVE ONE TEST IN BASKET APP DELIVERY CHANGE OPTIONS RADIO
# WE TEST IT HERE B

# TEST BASKET/VIEWS.PY basket_update_delivery
@pytest.mark.django_db
def test_basket_update_delivery(client, get_deliveries, get_basket):
    delivery = get_deliveries[0]
    url = reverse("basket:basket-update-delivery")
    data = {"action": "post", "deliveryoption": delivery.id}
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert response.json()['total'] == '25.73'
    assert response.json()['delivery_price'] == '5.99'
# END TEST BASKET/VIEWS.PY basket_update_delivery



# TEST delivery_address VIEW GET FOR MESSAGE IF NOT "PURCHASE" KEY IN SESSION
@pytest.mark.django_db
def test_delivery_address_view_get(client, get_customer):
    client.login(username = get_customer.email, password = 'qwerty')
    url = reverse("checkout:delivery_address")
    response = client.get(url, HTTP_REFERER = "http://127.0.0.1:8000/checkout/deliverychoices/")
    assert response.status_code == 302
    assert reverse("checkout:deliverychoices") in response.url
# END TEST delivery_address VIEW GET



# TEST DELIVERY_ADDRESS VIEW GET 
# BUL TEST "PURCHASE" KEY BOLADI SESSION DAT
@pytest.mark.django_db
def test_delivery_address_has_purchase_view_get(client, get_customer, get_address, get_basket_update_for_delivery_and_created_purchase_key):
    client.login(username = get_customer.email, password = "qwerty")
    address = get_address
    url = reverse("checkout:delivery_address")
    response = client.get(url)
    assert response.status_code == 200
    assert "Delivery Address".encode() in response.content
# END TEST DELIVERY_ADDRESS VIEW GET



# TEST GET CLIENT SECRET
@pytest.mark.django_db
def test_get_client_secret(client, get_customer, get_client_secret):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    intent, secret_key = get_client_secret
    url = reverse("checkout:pay")
    response = client.get(url)
    assert response.status_code == 200
    assert "Pay for your product".encode() in response.content
    assert intent['metadata']['userid'] == str(customer.id)
# END TEST GET CLIENT SECRET


# TEST PAY SECURELY VIEW GET FOR MESSAGE You didn't select your address
@pytest.mark.django_db
def test_pay_securely_view_get(client, get_created_address_key_in_session_defaul_false, get_address_default_false):
    url = reverse("checkout:pay")
    response = client.get(url, HTTP_REFERER = "http://127.0.0.1:8000/checkout/delivery_address/")
    assert response.status_code == 302
    assert reverse("checkout:delivery_address") in response.url
# END TEST PAY SECURELY VIEW GET



# TEST PAY SECURELY VIEW GET SUCCESS
@pytest.mark.django_db
def test_pay_securely_view_get_success(client, get_client_secret):
    intent, client_secret = get_client_secret
    url = reverse("checkout:pay")
    response = client.get(url)
    assert response.status_code == 200
    assert "Pay for your product".encode() in response.content
# END TEST PAY SECURELY VIEW GET SUCCESS