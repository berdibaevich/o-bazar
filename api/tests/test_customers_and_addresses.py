import pytest
from django.urls import reverse
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

from account.models import (
    Customer,
    Address
)
from api.serializers import (
    CustomerSerializers,
    AddressesSerializers,
    AddressDetailSerializers
)

# TEST CUSTOMERS API GET VIEW
@pytest.mark.django_db
def test_customers_api__get_view(api_client, get_customer_login, get_customer):
    url = reverse("api:customers")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
    customers = Customer.objects.filter(is_staff = False)
    serializer = CustomerSerializers(customers, many =True, context = {"request": response.wsgi_request})
    expected_response = {
        "customers": serializer.data,
        "num_of_customers": len(customers)
    }
    assert response.data == expected_response
# END TEST CUSTOMERS API GET VIEW



# TEST ADDRESSES API VIEW GET
@pytest.mark.django_db
def test_addresses_api_get_view(api_client, get_customer_login, get_customer, get_address):
    customer = get_customer
    url = reverse("api:customer-addresses", kwargs={"id": customer.id})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK

    addresses = get_list_or_404(Address.objects.select_related('customer'), customer__id = customer.id)
    serializer = AddressesSerializers(addresses, many = True, context = {"request": response.wsgi_request})
    expected_response = {
        "addresses": serializer.data
    }
    assert response.data == expected_response
# END TEST ADDRESSES API VIEW GET



# TEST ADDRESS DETAIL API VIEW GET
@pytest.mark.django_db
def test_address_api_get_view(api_client, get_customer, get_customer_login, get_address):
    address = get_address
    url = reverse("api:address-detail", kwargs={"id": address.id})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    
    address = get_object_or_404(Address, id = address.id)
    serializer = AddressDetailSerializers(address, many = False)
    expected_response = {
        "address_detail": serializer.data
    }
    assert response.data == expected_response
# END TEST ADDRESS DETAIL API VIEW GET