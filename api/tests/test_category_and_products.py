import pytest
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse
from inventory.models import (
    Category,
    Product,
    ProductInventory,
    Media
)
from api.serializers import (
    CategorySerializers,
    ProductSerializer,
    ProductInventorySerializers,
    MediaSerializers
)


# TEST CATEGORY API VIEW GET
@pytest.mark.django_db
def test_categories_api_view(api_client, get_categories, get_customer):
    customer = get_customer
    api_client.login(username = customer.email, password = "qwerty")
    url = reverse("api:category-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'next' in response.data
    assert 'previous' in response.data
# END TEST CATEGORY API VIEW GET



# TEST GET PRODUCTS API VIEW FOR CATEGORY PRODUCT TABLE 
@pytest.mark.django_db
def test_products_api_view_by_category(api_client, get_customer, get_product, category_with_child):
    customer = get_customer
    api_client.login(username = customer.email, password = "qwerty")
    new_category = category_with_child
    category = get_object_or_404(Category.objects.prefetch_related('children'), slug=new_category.slug)
    products = Product.objects.prefetch_related("category__children").filter(category__in = category.children.all())
    serializer = ProductSerializer(products, many = True, context = {'request': api_client})

    expexted_response = {
        "products": serializer.data,
        "number_of_products": len(products)
    }

    url = reverse("api:products-by-category", kwargs={"slug": new_category.slug})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expexted_response
# END TEST GET PRODUCTS API VIEW FOR CATEGORY PRODUCT TABLE 



# TEST GET PRODUCTS API VIEW FOR CATEGORY CHILD
@pytest.mark.django_db
def test_products_api_view_by_category_child(api_client, get_customer_login, get_product, category_with_child):
    category = category_with_child
    url = reverse("api:product-detail-by-categorychild", kwargs={"slug": category.slug})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    products = Product.objects.filter(category__slug = category.slug)
    serializer = ProductSerializer(products, many = True, context = {"request": response.wsgi_request})
    expected_response = {
        "products": serializer.data,
        "number_of_products": len(products)
    }
    assert response.data == expected_response
# TEST GET PRODUCTS API VIEW FOR CATEGORY CHILD



# TEST PRODUCT DETAIL API VIEW
@pytest.mark.django_db
def test_product_detail_api_view(api_client, get_customer_login, get_product, get_productinventory, get_productattributevalue):
    product = get_product
    url = reverse("api:product-detail", kwargs={'slug':product.slug})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    product = get_object_or_404(ProductInventory.objects.select_related("product", "brand"), product__slug = product.slug)
    serializer = ProductInventorySerializers(product, many = False, context = {"request": response.wsgi_request})
    expexted_response = {"product detail": serializer.data}
    assert response.data == expexted_response
# END TEST PRODUCT DETAIL API VIEW



# TEST MEDIA IMAGES 
@pytest.mark.django_db
def test_media_images_api_view(api_client, get_customer_login, get_productinventory, get_media):
    product = get_productinventory
    url = reverse("api:media-images", kwargs={"id": product.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    images = Media.objects.select_related("product_inventory").filter(product_inventory__id = product.id)
    serializer = MediaSerializers(images, many = True)
    expected_response = {
        'images': serializer.data
    }

    assert expected_response == response.data
# END TEST MEDIA IMAGES 