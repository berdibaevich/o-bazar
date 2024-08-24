import pytest
from django.urls import reverse


# TEST ALL PRODUCTS VIEW GET
@pytest.mark.django_db
def test_all_products_view_get(client, get_all_products):
    url = reverse("inventory:list-products")
    response = client.get(url)
    assert response.status_code == 200
    assert "Get in one click".encode() in response.content
# END TEST ALL PRODUCTS VIEW GET


# TEST ALL PRODUCTS VIEWS GET FOR SEARCH Q
@pytest.mark.django_db
def test_all_products_search_q(client, get_all_products):
    url = reverse("inventory:list-products")
    response = client.get(url, {"q": "oop"})
    assert "Python OOP".encode() in response.content
    assert len(response.context['products']) == 1
# END TEST ALL PRODUCTS VIEWS GET FOR SEARCH Q


# TEST ALL PRODUCTS VIEW GET SEARCH Q NONE EXISTS
@pytest.mark.django_db
def test_all_products_search_q_doesnt_exists(client, get_all_products):
    url = reverse("inventory:list-products")
    response = client.get(url, {"q": "ahjdhjauiaa"}, HTTP_REFERER = "http://127.0.0.1:8000/")
    assert response.status_code == 302
# END TEST ALL PRODUCTS VIEW GET SEARCH Q NONE EXISTS



# TEST PRODUCTS BY CATEGORY VIEW GET
@pytest.mark.django_db
def test_products_by_category_view_get(client, get_all_products, single_category):
    category = single_category
    url = reverse("inventory:products-by-category", kwargs={"slug": category.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "The Books".encode() in response.content
    assert len(response.context['products']) == 2
# END TEST PRODUCTS BY CATEGORY VIEW GET



# TEST PRODUCT BY CATEGORY CHILDREN VIEW GET
@pytest.mark.django_db
def test_products_by_category_child_view_get(client, get_all_products, get_category_childprogramming):
    category = get_category_childprogramming
    url = reverse("inventory:category-child", kwargs={"slug": category.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "The Programming".encode() in response.content
    assert len(response.context['products']) == 1
# END TEST PRODUCT BY CATEGORY CHILDREN VIEW GET



# TEST PRODUCT DETAIL VIEW GET
@pytest.mark.django_db
def test_product_detail_view_get(client, get_productinventory_for_programming, get_media_for_programming, get_product_for_programming):
    productinventory = get_product_for_programming
    url = reverse("inventory:product-detail", kwargs={"slug": productinventory.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "Add to basket".encode() in response.content
# END TEST PRODUCT DETAIL VIEW GET