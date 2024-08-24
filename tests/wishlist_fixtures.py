import pytest
from django.urls import reverse



# ADD TO WISHLIST SO WE USE IT
@pytest.fixture
def get_wishlist(db, client, get_productinventory_for_programming):
    product = get_productinventory_for_programming
    url = reverse("wishlist:add")
    data = {"action": "post", "product_id": get_productinventory_for_programming.id}
    response = client.post(url, data = data)
    return response 
# END ADD TO WISHLIST 

