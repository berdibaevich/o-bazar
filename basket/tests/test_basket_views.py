import pytest
from django.urls import reverse



# TEST BASKET LIST
@pytest.mark.django_db
def test_basket_list(client):
    url = reverse("basket:list")
    response = client.get(url)
    assert "Shopping basket".encode() in response.content
    assert response.status_code == 200
# END TEST BASKET LIST


# TEST ADD TO BASKET
@pytest.mark.django_db
def test_add_basket(client, get_productinventory):
    url = reverse("basket:add_to_basket")
    data = {"action": "post", "product_id": get_productinventory.id, "product_quantity": "2"}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.json()['total_qty'] == 2
# END TEST ADD TO BASKET


# TEST UPDATE BASKET
@pytest.mark.django_db
def test_update_basket(client, get_productinventory, get_basket):
    url = reverse("basket:update_basket")
    data = {"action": "post", "product_id": get_productinventory.id, "product_quantity": "5"}
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert response.json()['total_price'] == '49.35'
    assert response.json()['total_qty'] == 5
# END TEST UPDATE BASKET


# TEST DELETE BASKET
@pytest.mark.django_db
def test_delete_basket(client, get_productinventory, get_basket):
    url = reverse("basket:delete_basket")
    data = {"action": "post", "product_id": get_productinventory.id}
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert response.json()['total_price'] == 0
    assert response.json()['total_qty'] == 0
# END TEST DELETE BASKET


# TEST DELIVERY OPTION BASKET WRITTEN TO CHECKOUT APP TEST_VIEWS.PY 