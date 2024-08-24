import pytest
from account.forms import (
    RegisterForm,
    UserLoginForm,
    UserEditForm,
    UserAddressForm
)


# TEST REGISTERFORM
@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "qwerty1234", "qwerty1234", True),
        ("user1", "a@b.com", "qwerty12345", "", False), #no second password here
        ("user2", "", "qwerty123457", "qwerty123457", False), #no email error
        ("user2", "a@c.com", "qwerty12345", "qwerty12", False), #password doesn't match
    ], 
)
@pytest.mark.django_db
def test_create_account_by_form(client,user_name, email, password, password2, validity):
    form = RegisterForm(
        data = {
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2
        }
    )
 
    assert form.is_valid() == validity
# END TEST REGISTERFORM



# TEST USERLOGINFORM
@pytest.mark.parametrize(
    "username, password, validity",
    [
        ("a@a.com", "qwerty", True), # This is True because we gonna create new customer account bellow
        ("a@a.com", "", False),
        ("a@b.com", "12345678", False),
    ]
)
@pytest.mark.django_db
def test_user_loginform(client, username, password, validity, get_customer):
    customer = get_customer #This is create new customer account
    form = UserLoginForm(
        data = {
            "username": username,
            "password": password
        }
    )
    assert form.is_valid() == validity
# END TEST USERLOGINFORM



# TOMENDE KORIP SHIGIWIMIZ KEREK

# TEST USER EDIT FORM
@pytest.mark.parametrize(
    "email, user_name, phone_number, validity",
    [
        ("a@a.com","John English", "905973467", True),
        ("a@a.com","John English", "", False),
        ("a@a.com","", "12347812", False)
    ]
)
@pytest.mark.django_db
def test_user_edit_form(client, email, user_name, phone_number, validity):

    form = UserEditForm(
        data = {
            "email": email,
            "user_name": user_name,
            "phone_number": phone_number
        },
    )
    assert form.is_valid() == validity
# END TEST USER EDIT FORM



# TEST USER ADDRESS FORM
@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, validity",
    [
        ("user1 full name", "12348923", "usa", "new york", "nukus", "12390", True),
        ("user2 full name", "", "usa", "new york", "nukus", "12390", False),
        ("user3 full name", "123892231", "usa", "new york", "nukus", "", False),
        ("user4 full name", "123892232", "", "new york", "nukus", "12363", False),
        ("user5 full name", "12389223", "mayami", "new york", "", "123632", False),
        ("user6 full name", "", "mayami", "new york", "", "123632", False),
        ("", "12390023", "Shimbay", "new york", "Guzar city", "123632", False),
    ]
)
@pytest.mark.django_db
def test_user_address_form(client, full_name, phone, address_line, address_line2, town_city, postcode, validity):
    form = UserAddressForm(
        data = {
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode
        }
    )
    assert form.is_valid() == validity
# END TEST USER ADDRESS FORM

