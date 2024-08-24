from inventory.models import (
    Category,
)
import pytest


# TEST CATEGORY TABLE 


#  TEST CREATE CATEGORY SINGLE
#@pytest.mark.skip
def test_create_category(single_category):
    new_category = single_category
    get_category = Category.objects.all().first()
    assert get_category.id == new_category.id
    assert get_category.name == new_category.name
    assert get_category.slug == new_category.slug
# END CREATE TEST CATEGORY SINGLE


# TEST CREATE CATEGORY WITH CHILD
def test_create_category_with_child(category_with_child):
    get_category = Category.objects.first()
    category_child = category_with_child
    assert get_category.children.first().name == category_child.name
    assert get_category.children.first().slug == category_child.slug
    assert category_child.parent.name == get_category.name
# END CREATE TEST CATEGORY WITH CHILD





# END TEST CATEGORY TABLE 

















