import pytest
from account.models import (
    Customer,
    Address
)


# CUSTOMER TABLE FIXTURES FOR ADMIN
@pytest.fixture
def get_admin(db):
    return Customer.objects.create_superuser("admin@gmail.com", "admin", "qwerty")
# END CUSTOMER TABLE FIXTURES FOR ADMIN


# CUSTOMER TABLE FIXTURES FOR CUSTOMER
@pytest.fixture
def get_customer(db):
    customer = Customer.objects.create(email = "a@a.com", user_name = "John", is_active = True)
    customer.set_password("qwerty")
    customer.save()
    return customer
# END CUSTOMER TABLE FIXTURES FOR CUSTOMER


# ADDRESS TABLE FIXTURES
@pytest.fixture
def get_address(db, get_customer):
    customer = get_customer
    address = Address.objects.create(
        customer = customer,
        full_name = "John English",
        phone = "905678930",
        postcode = "108923",
        address_line = "USA",
        address_line2 = "New York",
        town_city = "Nukus",
        default = True
    )
    return address
# END ADDRESS TABLE FIXTURES


# ADDRESS TABLE FIXTURES DEFAULT FALSE
@pytest.fixture
def get_address_default_false(db, get_customer):
    customer = get_customer
    address = Address.objects.create(
        customer = customer,
        full_name = "John English",
        phone = "905678930",
        postcode = "108923",
        address_line = "USA",
        address_line2 = "New York",
        town_city = "Nukus",
        default = False
    )
    return address
# END ADDRESS TABLE FIXTURES DEFAULT FALSE