import pytest
from django.urls import reverse



# GET BASKET SESSION DATA
@pytest.fixture
def get_basket(db, client, get_productinventory):
    url = reverse("basket:add_to_basket")
    data = {"action": "post", "product_quantity": "2", "product_id": get_productinventory.id}
    response = client.post(url, data = data)
    return response
# END GET BASKET SESSION DATA