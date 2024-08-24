import stripe
import pytest
from checkout.models import Delivery
from django.urls import reverse
from django.conf import settings


# GET DELIVERY FOR TEST
@pytest.fixture
def get_deliveries(db):
    Delivery.objects.create(
        delivery_name = "FedEx",
        delivery_price = 5.99,
        delivery_method = "HM",
        delivery_timeframe = "1-2 days",
        delivery_window = "9.00am : 9.00pm",
        order = 3
    )
    Delivery.objects.create(
        delivery_name = "Parcel Delivery",
        delivery_price = 4.77,
        delivery_method = "HM",
        delivery_timeframe = "3-4 days",
        delivery_window = "9.00am : 9.00pm",
        order = 2
    )
    return Delivery.objects.all()
# END GET DELIVERY



# GET PURCHASE KEY CREATED IN SESSION 
@pytest.fixture
def get_basket_update_for_delivery_and_created_purchase_key(db, client, get_deliveries, get_basket):
    delivery = get_deliveries[0]
    url = reverse("basket:basket-update-delivery")
    data = {"action": "post", "deliveryoption": delivery.id}
    response = client.post(url, data)
    return response
# END GET PURCHASE KEY CREATED IN SESSION 



# GET ADDRESS KEY IN SESSION
@pytest.fixture
def get_created_address_key_in_session(db, client, get_basket_update_for_delivery_and_created_purchase_key, get_customer, get_address):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    url = reverse("checkout:delivery_address")
    response = client.get(url) 
# END GET ADDRESS KEY IN SESSION 



# GET CLIENT SECRET
@pytest.fixture
def get_client_secret(db, client, get_created_address_key_in_session, get_basket_update_for_delivery_and_created_purchase_key, get_customer):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    total_price = int(get_basket_update_for_delivery_and_created_purchase_key.json()['total'].replace(".", ""))
    SECRET_KEY = settings.SECRET_KEY
    url = reverse("checkout:pay")
    response = client.get(url)
    intent = stripe.PaymentIntent.create(
        amount = total_price,
        currency = "usd",
        metadata = {'userid': customer.id}
    )
    return intent, intent.client_secret
# END GET CLIENT SECRET



# GET ADDRESS KEY IN SESSION BUT DEFAULT FALSE FOR MESSAGE
@pytest.fixture
def get_created_address_key_in_session_defaul_false(db, client, get_basket_update_for_delivery_and_created_purchase_key, get_customer, get_address_default_false):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    url = reverse("checkout:delivery_address")
    response = client.get(url) 
# END GET ADDRESS KEY IN SESSION BUT DEFAULT FALSE FOR MESSAGE