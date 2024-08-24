import pytest
from django.urls import reverse
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from checkout.models import Delivery
from api.serializers import (
    DeliveryDetailSerializers,
    DeliveryListSerializers
)


# TEST DELIVERY LIST API VIEW
@pytest.mark.django_db
def test_deliveries_api_view_get(api_client, get_customer_login, get_deliveries):
    url = reverse("api:delivery-list")
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK

    deliveries = Delivery.objects.all()
    serializer = DeliveryListSerializers(deliveries, many = True, context = {"request": response.wsgi_request})
    expected_response = {
        "deliveries": serializer.data,
        "num_of_deliveries": len(deliveries)
    }
    assert response.data == expected_response
# END TEST DELIVERY LIST API VIEW


# TEST DELIVERY DETAIL API VIEW GET
@pytest.mark.django_db
def test_delivery_detail_api_view_get(api_client, get_customer_login, get_deliveries):
    delivery = get_deliveries[0]
    url = reverse("api:delivery-detail", kwargs={"id": delivery.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    delivery = get_object_or_404(Delivery, id = delivery.id)
    serializer = DeliveryDetailSerializers(delivery, many = False)

    assert response.data == serializer.data
# END TEST DELIVERY DETAIL API VIEW GET