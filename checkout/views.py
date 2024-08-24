from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from basket.basket import Basket
from .models import Delivery
from account.models import Address
import stripe
# Create your views here.

# DELIVERY CHOICES
@login_required
def deliverychoices(request):
    deliveryoptions = Delivery.objects.filter(is_active = True)
    context = {
        'deliveryoptions': deliveryoptions
    }
    return render(request, 'checkout/delivery_choices.html', context)
# END DELIVERY CHOICES


# DELIVERY ADDRESS
@login_required
def delivery_address(request):
    session = request.session

    if 'purchase' not in request.session:
        messages.info(request, "Please select delivery option.")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    addresses = Address.objects.filter(customer = request.user).order_by('-default')
    if addresses:
        if 'address' not in request.session:
            session['address'] = {'address_id': str(addresses[0].id)}
        else:
            session['address']['address_id'] = str(addresses[0].id)
            session.modified = True

    context = {
        'addresses': addresses
    }
    return render(request, 'checkout/delivery_address.html', context)
# END DELIVERY ADDRESS


# GET CLIENT SECRET
def get_client_secret(request):
    basket = Basket(request)
    total_price = str(basket.get_total_and_delivery_price()).replace(".", "")
    total_price_int = int(total_price)
    stripe.api_key = "sk_test_51MOjpRDh4Pu0qkGJK8Qe4I9X2GERDaEV62lSzW1FLC4dDoBnp35fOzvjzW2ErnnRPmFTjR5RpURp1RgudjEjoZ9100xlkFvlQ2"
    intent = stripe.PaymentIntent.create(
        amount = total_price_int,
        currency = "usd",
        metadata = {'userid': request.user.id}
    )
    return intent.client_secret
# END GET CLIENT SECRET



# PAY YOUR PRODUCT 
@login_required
def pay_securely(request):
    address_id = request.session.get('address')['address_id']
    delivery_id = request.session.get("purchase")['delivery_id']
    delivery = Delivery.objects.get(id = delivery_id)
    address = Address.objects.filter(id =address_id,customer = request.user, default = True).first()
    if not address:
        previous_url = request.META.get("HTTP_REFERER")
        if "delivery_address" in previous_url:
            messages.warning(request, "You didn't select your address.Select your address.")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # GET CLIENT SECRET
    client_secret = get_client_secret(request)
        
    context = {
        "address": address,
        "delivery":delivery,
        "client_secret": client_secret
    }
    return render(request, 'checkout/pay_securely.html', context)
# END PAY YOUR PRODUCT

