import pytest
from account.models import Customer, Address
from account.forms import UserAddressForm
from django.urls import reverse

# BELLOW LOGGING --> I HAVE NO IDEA WHY I SET THIS SO 
# IF YOU WANT TO KNOW PLEASE TEST THIS FILE BEFORE TEST BELLOW IMPORT LOGGING REMOVE
# THEN TEST IT YOU CAN SEE IN CONSOLE COMES UP MESSAGE LIKE WARNING OK :)
import logging
logger = logging.getLogger('django.request')
logger.setLevel(logging.ERROR)



# TEST CREATE ACCOUNT VIEW
@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "qwerty123", "qwerty123", 200),
        ("user1", "a@a.com", "qwerty", "qwerty123", 400),
        ("user1", "", "qwerty123", "qwerty123", 400),
    ]
)
# validity 200 if is valid or 400 error comes up so check out your view account_register
@pytest.mark.django_db
def test_create_account_view(client, user_name, email, password, password2, validity):
    response = client.post(
        "/account/sign-up/",
        data = {
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2
        }
    )
    assert response.status_code == validity
# END TEST CREATE ACCOUNT VIEW



# TEST ACCOUNT LOGIN VIEW Yag'niy login qiliw proccessi ok :)
@pytest.mark.parametrize(
    "username, password, validity",
    [
        ("a@a.com", "qwerty", 200),
        ("a@b.com", "qwerty", 302),
    ]
)
@pytest.mark.django_db
def test_account_loginview(client, username, password, validity, get_customer):
    client.login(username = username, password = password)
    url = reverse("account:dashboard")
    response = client.get(url)
    assert response.status_code == validity
# END TEST ACCOUNT LOGIN VIEW


# TEST DASHBOARD VIEW
@pytest.mark.django_db
def test_dashboard_view_get(client, get_customer):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    url = reverse("account:dashboard")
    response = client.get(url)
    assert response.status_code == 200
    assert "Your Dashboard".encode() in response.content
# END TEST DASHBOARD VIEW



# TEST EDIT PROFILE
@pytest.mark.parametrize(
    "email, user_name, phone_number, validity",
    [
        ("a@a.com", "John English", "3489212312", 200),
        ("a@a.com", "John English", "3489", 400), #Phone number is short it gives you status 400 check out view of this func
        ("a@a.com", "", "34891231312", 400), #User name doesn't fill out
        ("a@b.com", "JoHn", "34891231312", 302), #Wrong email so he is not login 
    ]
)
@pytest.mark.django_db
def test_edit_form_view(client, email, user_name, phone_number, validity, get_customer):
    client.login(username = email, password = "qwerty")
    response = client.post(
        "/account/edit-profile/",
        data = {
            "email": email,
            "user_name": user_name,
            "phone_number": phone_number
        },
    )
    assert response.status_code == validity
# END TEST EDIT PROFILE 



# TEST DELETE ACCOUNT VIEW PROCCESS
@pytest.mark.parametrize(
    "email, password, validity",
    [
        ("a@a.com", "qwerty", 200)
    ]
)
@pytest.mark.django_db
def test_delete_account_view(client, email, password, validity, get_customer):
    client.login(username = email, password = password)
    response = client.post(reverse("account:delete-account"))
    response_url = reverse("account:delete_confirmation")
    customers = Customer.objects.filter(is_active = True)
    assert len(customers) == 0
    assert response.url == response_url
# END TEST DELETE ACCOUNT VIEW PROCCESS




# TEST VIEW ADDRESS
@pytest.mark.django_db
def test_view_address(client, get_customer, password = "qwerty"):
    customer = get_customer
    client.login(username = customer.email, password = password)
    get_address = client.post(reverse("account:addresses"))
    text_for_check = "Your Addresses".encode()
    assert get_address.status_code == 200
    assert text_for_check in get_address.content
# END TEST VIEW ADDRESS



# TEST ADD ADDRESS
@pytest.mark.parametrize(
    'full_name, phone, address_line, address_line2, town_city, postcode, validity',
    [
        ("Bitz", "12345678", "New York", "USA", "Nukus", "12345", False),
        ("Bitz", "12345678", "New York", "USA", "Nukus", "", True),
        ("Bitz", "12345678", "", "USA", "Nukus", "123892", True)
    ]
)
@pytest.mark.django_db
def test_add_address(client, full_name, phone, address_line, address_line2, town_city, postcode, validity, get_customer):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    response = client.post(
        reverse("account:add-address"),
        data = {
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode
        }
    )

    # CHECK MESSAGES ERROR !
    message_error = "Please try again!".encode()
    is_error = message_error in response.content
    assert is_error == validity
    # END CHECK MESSAGES ERROR !
    if not validity:
        next_page = reverse("account:addresses")
        assert next_page == response.url
# END TEST ADD ADDRESS



# TEST EDIT ADDRESS VIEW GET
@pytest.mark.django_db
def test_edit_address_view_get(client, get_customer, get_address):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    address = get_address
    url = reverse("account:edit-address", kwargs={'id': address.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'form'.encode() in response.content
    assert isinstance(response.context['form'], UserAddressForm)
# END TEST EDIT ADDRESS VIEW GET



# TEST EDIT ADDRESS VIEW POST
# This is skipped because I have no idea
@pytest.mark.skip
@pytest.mark.django_db
def test_edit_address_view_post(client, get_customer, get_address):
    customer = get_customer
    client.login(username = customer.email, password = "qwerty")
    address = get_address
    url = reverse("account:edit-address", kwargs={"id": address.id})
    data = {
        "full_name": "John English ENG",
        "town_city": "Nukus Qalam"
    }
    response = client.post(url, data=data)
# END TEST EDIT ADDRESS VIEW POST



# TEST DELETE ADDRESS VIEW DELETE
@pytest.mark.django_db
def test_delete_address_view_delete(client, get_customer, get_address):
    customer = get_customer
    address = get_address
    client.login(username = customer.email, password = "qwerty")
    url = reverse("account:delete-address", kwargs={"id": address.id})
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse("account:addresses")
# END TEST DELETE ADDRESS VIEW DELETE



# TEST SET DEFAULT VIEW ADDRESS URL FOR ACCOUNT ADDRESSES REQUEST
@pytest.mark.django_db
def test_set_default(client, get_customer, get_address):
    """
     This set_defult request previous_url is http://127.0.0.1:8000/account/addresses/
    """
    customer = get_customer
    address = get_address
    client.login(username = customer.email, password = "qwerty")
    url = reverse("account:set-default", kwargs={"id": address.id})
    Address.objects.filter(customer = customer, default = True).update(default = False)
    response = client.post(url, HTTP_REFERER = "http://127.0.0.1:8000/account/addresses/")
    assert response.status_code == 302
    assert response.url == reverse("account:addresses")
# END TEST SET DEFAULT VIEW ADDRESS



# TEST SET DEFAULT VIEW ADDRESS URL FOR checkout:delivery_address
@pytest.mark.django_db
def test_set_default_for_checkout_url(client, get_customer, get_address):
    customer = get_customer
    address = get_address
    client.login(username = customer.email, password = "qwerty")
    url = reverse("account:set-default", kwargs={"id": address.id})
    Address.objects.filter(customer = customer, default = True).update(default = False)
    response = client.post(url, HTTP_REFERER = "http://127.0.0.1:8000/checkout/delivery_address/")
    assert response.status_code == 302
    assert response.url == reverse("checkout:delivery_address")
# END TEST SET DEFAULT VIEW ADDRESS URL FOR checkout:delivery_address


