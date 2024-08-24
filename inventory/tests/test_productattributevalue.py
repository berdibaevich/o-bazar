from inventory.models import ProductAttributeValue



# TEST PRODUCTATTRIBUTEVALUE TABLE


# TEST CREATE PRODUCTATTRIBUTEVALUE
def test_productattributevalue(get_productattributevalue):
    new_productattributevalue = get_productattributevalue
    productattributevalue = ProductAttributeValue.objects.first()
    assert productattributevalue.__str__() == new_productattributevalue.__str__()
    assert productattributevalue.attribute_name == new_productattributevalue.attribute_name
    assert productattributevalue.attribute_value == str(new_productattributevalue.attribute_value)
# END TEST CREATE PRODUCTATTRIBUTEVALUE




# END TEST PRODUCTATTRIBUTEVALUE TABLE 