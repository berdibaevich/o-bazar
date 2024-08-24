from inventory.models import Brand


# TEST BRAND TABLE

# TEST CREATE BRAND 
def test_create_brand(get_brand):
    brand = Brand.objects.first()
    new_brand = get_brand
    assert new_brand.id == brand.id 
    assert new_brand.name == brand.name 
# END TEST CREATE BRAND


# END TEST BRAND TABLE 