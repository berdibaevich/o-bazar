from inventory.models import Product


# TEST PRODUCT TABLE

# TEST CREATE PRODUCT
def test_create_product(get_product):
    product = Product.objects.first()
    new_product = get_product
    product_cats = product.category.all()
    assert new_product.name == product.name
    assert new_product.slug == product.slug
    assert len(product_cats) == 1
# TEST CREATE PRODUCT



# END TEST PRODUCT TABLE