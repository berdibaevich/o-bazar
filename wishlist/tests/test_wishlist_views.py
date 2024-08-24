import pytest
from django.urls import reverse


# TEST GET WISHLIST VIEW GET PAGE WILL BE EXPECTED NO PRODUCTS IN YOUR WISHLIST
@pytest.mark.django_db
def test_get_wishlist_view_get_no(client):
    url = reverse("wishlist:list")
    response = client.get(url)
    assert response.status_code == 200
    assert "No products have been added to your wishlist yet".encode() in response.content
# END TEST GET WISHLIST VIEW GET



# TEST WISHLIST ADD FROM HOME PAGE
@pytest.mark.django_db
def test_add_to_wishlist(client, get_productinventory_for_programming):
    product = get_productinventory_for_programming
    url = reverse("wishlist:add")
    data = {"action": "post", "product_id": product.id}
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert response.json()['how_many'] == 1
# END TEST WISHLIST ADD FROM HOME PAGE


# TEST WISHLIST REMOVE FROM HOME PAGE
@pytest.mark.django_db
def test_remove_from_wishlist(client, get_wishlist, get_productinventory_for_programming):
    product = get_productinventory_for_programming
    url = reverse("wishlist:add")
    data = {"action": "post", "product_id": product.id}
    response = client.post(url, data = data)
    assert response.status_code == 200
    assert response.json()['how_many'] == 0
    assert client.session['wishlist'] == {}
# END TEST WISHLIST REMOVE FROM HOME PAGE