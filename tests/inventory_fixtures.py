import pytest
from inventory.models import (
    Category,
    Product,
    Brand,
    ProductInventory,
    Media,
    ProductAttributeValue
)

# SINGLE CATEGORY FIXTURES
@pytest.fixture
def single_category(db):
    return Category.objects.create(
        name = "The Books", slug = "the-books"
    )
# END SINGLE CATEGORY FIXTURES



# CATEGORY WITH CHILD FIXTURES
@pytest.fixture
def category_with_child(db, single_category):
    parent_category = single_category
    return Category.objects.create(
        name = "Biznes kitaplar", slug = "biznes-kitaplar",
        parent = parent_category
    )
# END CATEGORY WITH CHILD FIXTURES



# PRODUCT TABLE FIXTURES
@pytest.fixture
def get_product(db, category_with_child):
    category = category_with_child
    product = Product.objects.create(
        name = "Never give up haha",
        slug = "never-give-up-haha",
        description = "cool is cool",
    )
    product.category.add(category)
    return product
# END PRODUCT TABLE FIXTURES



# BRAND TABLE FIXTURES
@pytest.fixture
def get_brand(db):
    return Brand.objects.create(name = "The Bookshelf")
# END BRAND TABLE FIXTURES



# PRODUCTINVENTORY TABLE FIXTURES
@pytest.fixture
def get_productinventory(db, get_product, get_brand):
    product = get_product
    brand = get_brand
    productinventory = ProductInventory.objects.create(
        upc = "1234567",
        product = product,
        brand = brand,
        sale_price = 9.87
    )
    return productinventory
# END PRODUCTINVENTORY TABLE FIXTURES



# MEDIA TABLE FIXTURES
@pytest.fixture
def get_media(db, get_productinventory):
    productinventory = get_productinventory
    media = Media.objects.create(
        product_inventory = productinventory,
        alt_text = 'cool',
        is_feature = True
    )
    return media
# END MEDIA TABLE FIXTURES



# ProductAttributeValue TABLE FIXTURES
@pytest.fixture
def get_productattributevalue(db, get_productinventory):
    productinventory = get_productinventory
    productattributevalue = ProductAttributeValue.objects.create(
        product_inventory = productinventory,
        attribute_name = "Page",
        attribute_value = 544
    )
    return productattributevalue
# END ProductAttributeValue TABLE FIXTURES




# GET CATEGORY PARENT NAME PROGRAMMING
@pytest.fixture
def get_category_childprogramming(db, single_category):
    parent_category = single_category
    return Category.objects.create(
        name = "The Programming", slug = "the-programming",
        parent = parent_category
    )
# END GET CATEGORY PARENT PROGRAMMING



# GET PRODUCT FOR PROGRAMMING CATEGORY CHILD
@pytest.fixture
def get_product_for_programming(db, get_category_childprogramming):
    category = get_category_childprogramming
    product = Product.objects.create(
        name = "Python OOP",
        slug = "python-oop",
        description = "python for everybody",
    )
    product.category.add(category)
    return product
# END GET PRODUCT FOR PROGRAMMING CATEGORY CHILD



# GET PRODUCT INVENTORY FOR PYTHON OOP BOOK NAME
@pytest.fixture
def get_productinventory_for_programming(db, get_product_for_programming, get_brand):
    product = get_product_for_programming
    brand = get_brand
    productinventory = ProductInventory.objects.create(
        upc = "123456712",
        product = product,
        brand = brand,
        sale_price = 10.99
    )
    return productinventory
# END GET PRODUCT INVENTORY FOR PYTHON OOP BOOK NAME



# MEDIA TABLE FIXTURES FOR PYTHON OOP
@pytest.fixture
def get_media_for_programming(db, get_productinventory_for_programming):
    productinventory = get_productinventory_for_programming
    media = Media.objects.create(
        product_inventory = productinventory,
        alt_text = 'cool1',
        is_feature = True
    )
    return media
# END MEDIA TABLE FIXTURES



# ProductAttributeValue TABLE FIXTURES
@pytest.fixture
def get_productattributevalue_for_programming(db, get_productinventory_for_programming):
    productinventory = get_productinventory_for_programming
    productattributevalue = ProductAttributeValue.objects.create(
        product_inventory = productinventory,
        attribute_name = "Page",
        attribute_value = 358
    )
    return productattributevalue
# END ProductAttributeValue TABLE FIXTURES



# GET PRODUCTINVENTORY FOR ALL PRODUCTS VIEW
@pytest.fixture
def get_all_products(db, get_productattributevalue_for_programming, get_media_for_programming, get_productattributevalue, get_media):
    products = ProductInventory.objects.all()
    return products
# END GET PRODUCTINVENTORY FOR ALL PRODUCTS