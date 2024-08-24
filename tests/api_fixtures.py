import pytest
from inventory.models import (
    Category,

)
from api.serializers import (
    CategorySerializers
)


# FOR CATEGORY FIXTURES
@pytest.fixture
def get_categories(db):
    category1 = Category.objects.create(name = "Books", slug = 'books')
    category2 = Category.objects.create(name = "Python OOP", slug = 'python-oop', parent = category1)
    category3 = Category.objects.create(name = "Django ORM", slug = 'django-orm', parent = category1)
    return [category1, category2, category3]


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_customer_login(db, api_client, get_customer):
    customer = get_customer
    api_client.login(username = customer.email, password = 'qwerty')
    return True


# END FOR CATEGORY FIXTURES

