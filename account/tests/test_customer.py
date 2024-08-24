from account.models import Customer


# TEST CUSTOMER TABLE

# TEST CREATE ADMIN
def test_create_admin(get_admin):
    admin = get_admin
    customer = Customer.objects.first()
    assert customer.is_staff == True
    assert customer.is_superuser == True
    assert customer.is_active == True
    assert admin.user_name == customer.user_name
    assert customer.password == admin.password
# END TEST CREATE ADMIN 


# TEST CREATE CUSTOMER
def test_create_customer(get_customer):
    new_customer = get_customer
    customer = Customer.objects.first()
    assert new_customer.is_active == True
    assert new_customer.id == customer.id
# END TEST CREATE CUSTOMER




# END TEST CUSTOMER TABLE 
