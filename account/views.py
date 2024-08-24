from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Customer, Address
from .forms import (
    RegisterForm,
    UserEditForm,
    UserAddressForm,
)

# SETUP E-MAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from .token import account_activation_token
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


# ACCOUNT REGISTER
def account_register(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data.get('email')
            user.set_password(registerform.cleaned_data['password'])
            user.is_active = True #Because doesn't work Gmail when after deployed
            user.save()
            # ADD LOGIN AND REDIRECT ALSO CHANGED IS_ACTIVE = TRUE 
            # WHY BEACUSE WHEN DEPLOYED GMAIL MESSAGE DOESN'T WORK
            login(request, user)
            return redirect('account:dashboard')

            # SETUP E-mail
            # current_site = get_current_site(request)
            # subject = "Active your Account"
            # message = render_to_string(
            #     "account/account_activation_email.html",
            #     {
            #         'user': user,
            #         'domain': current_site.domain,
            #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #         'token': account_activation_token.make_token(user),

            #     })
            
            # #user.email_user(subject=subject, message = message)
            # from_email = settings.EMAIL_HOST_USER
            # recipient_list = [user.email]
            # send_mail(subject, message, from_email, recipient_list)
            # return HttpResponse('Registered successfully, so check out your account Gmail to activate your account.')
        
        # else:
        #     return HttpResponse("Error try again.", status=400)

    else:
        registerform = RegisterForm()

    context = {
        "form": registerform
    }
    return render(request, 'account/register.html', context)
# END ACCOUNT REGISTER


# ACCOUNT ACTIVATE
def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk = uid)
    except:
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
        
    else:
        return render(request, 'account/activation_invalid.html')
# END ACCOUNT ACTIVATE
        

#DASHBOARD
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')
# END DASHBOARD


# EDIT USER INFO VIEWS
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(instance = request.user, data=request.POST)
        if form.is_valid():
            form.save()
        # else:
        #     return HttpResponse("Fill out this form", status = 400)
    else:
        form = UserEditForm(instance = request.user)
    context = {
        'form': form
    }
    return render(request, 'account/edit_profile.html', context)
# END EDIT USER INFO VIEWS


# DELETE ACCOUNT
@login_required
def delete_account(request):
    user = get_object_or_404(Customer, user_name = request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')
# END DELETE ACCOUNT




#                   ADDRESSES SET UP

# VIEWS ADDRESS
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer = request.user)
    context = {
        'addresses': addresses
    }
    return render(request, 'account/address/addresses.html', context)
# END VIEWS ADDRESS


# ADD ADDRESS
@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data = request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))

    else:
        address_form = UserAddressForm()
    
    context = {
        'form': address_form
    }
    return render(request, 'account/address/add_address.html', context)
# END ADD ADDRESS


# EDIT ADDRESS
def edit_address(request, id):
    if request.method == 'POST':
        address = Address.objects.get(pk = id, customer = request.user)
        address_form = UserAddressForm(instance = address, data = request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk = id, customer = request.user)
        address_form = UserAddressForm(instance = address)

    context = {
        'form': address_form
    }
    return render(request, 'account/address/edit_address.html', context)
# END EDIT ADDRESS


# DELETE ADDRESS
def delete_address(request, id):
    address = Address.objects.get(pk = id, customer = request.user).delete()
    return redirect("account:addresses")
# END DELETE ADDRESS


# SET DEFAULT ADDRESS
def set_default(request, id):
    Address.objects.filter(customer = request.user, default = True).update(default = False)
    Address.objects.filter(pk = id, customer = request.user).update(default = True)
    
    previous_url = request.META.get("HTTP_REFERER")
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")
# END SET DEFAULT ADDRESS


# GET API PAGE
@login_required
def get_api_page(request):
    return render(request, 'account/api_page.html')
# END GET API PAGE









