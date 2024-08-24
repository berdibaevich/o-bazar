from django import forms
from .models import Customer, Address
from django.contrib.auth.forms import AuthenticationForm

# REGISTER FORM
class RegisterForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Enter Username", min_length=4, max_length=20,
        help_text="Required"
    )

    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)


    
    def clean_username(self):
        """
        Check Username if username doest exists then save into db
        or give him some error
        """
        user_name = self.cleaned_data['user_name'].lower()
        exists = Customer.objects.filter(user_name=user_name)
        if exists.exists():
            raise forms.ValidationError('Username already exists!')
        
        return user_name

    
    def clean_password2(self):
        """
        Check two password
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match")
        
        return cd



    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email, that is already taken'
            )
        
        return email

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'}
        )
# END REGISTER FORM



# LOGIN FORM
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control mb-3",
            "placeholder": "Username",
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password', 
            'id': 'login-password'
        }
    ))
# END LOGIN FORM



# EDIT USER INFO
class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Email',
                'id': 'form-email',
                'readonly': 'readonly'
            }
        )

    )

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=40, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'UserName',
                'id': 'form-username',
                
            }
        )
    )
    phone_number = forms.CharField(
        label='Phone Number', min_length=9, max_length=40, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Phone Number',
                'id': 'form-phonenumber',
                
            }
        )
    )

    class Meta:
        model = Customer
        fields = ('email', 'user_name', 'phone_number')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['email'].required = True
# END EDIT USER INFO

    

#Add address form
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_name', 'phone', 'address_line', 'address_line2', 'town_city', 'postcode')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('full_name').widget.attrs.update(
            {
                'class': 'form-control mb-3 address-form',
                'placeholder': 'Full Name'
            }
        )

        self.fields.get('phone').widget.attrs.update(
            {
                'class': 'form-control mb-3 address-form',
                'placeholder': 'phone'
            }
        )

        self.fields.get('address_line').widget.attrs.update(
            {
                'class': 'form-control mb-3 address-form',
                'placeholder': 'Address'
            }
        )

        self.fields.get('address_line2').widget.attrs.update(
            {
                'class': 'form-control mb-3 address-form',
                'placeholder': 'Address 2'
            }
        )

        self.fields.get('town_city').widget.attrs.update(
            {
                'class': 'form-control mb-3 address-form',
                'placeholder': 'Town, City'
            }
        )

        self.fields.get('postcode').widget.attrs.update(
            {
                'class': 'form-control mb-3 address-form',
                'placeholder': 'PostCode'
            }
        )