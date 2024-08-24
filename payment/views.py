from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from basket.basket import Basket
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from orders.views import payment_confirmation
from inventory.models import ProductInventory
from checkout.models import Delivery
# Create your views here.



# STRIPE WEBHOOK
@csrf_exempt
def stripe_webhook(request):
    paylaod = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(paylaod), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status = 400)

    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print(f'Unhandled event type {event.type}')
    return HttpResponse(status = 200)
# END STRIPE WEBHOOK


# CLEAR purchase FROM SESSION AS DELIVERY
def clear_purchase(request):
    if "purchase" in request.session:
        del request.session['purchase']
# END CLEAR purchase FROM SESSION

# CLEAR ADDRESS FROM SESSION
def clear_address(request):
    if "address" in request.session:
        del request.session["address"]
# END CLEAR ADDRESS FROM SESSION


# ORDER PLACED
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    clear_purchase(request)
    clear_address(request)
    return render(request, 'payment/orderplaced.html')
# END ORDER PLACED




# GET CLIENT SECRET KEY
def get_client_secretkey(amount, user_id, currency = "usd"):
    stripe.api_key = "sk_test_51MOjpRDh4Pu0qkGJK8Qe4I9X2GERDaEV62lSzW1FLC4dDoBnp35fOzvjzW2ErnnRPmFTjR5RpURp1RgudjEjoZ9100xlkFvlQ2"
    intent = stripe.PaymentIntent.create(
        amount = amount,
        currency = currency,
        metadata = {'userid': user_id}
    )
    return intent.client_secret
# END GET CLIENT SECRET KEY



# GETTING IN ONE CLICK
@login_required
def payment_one_click(request, slug):
    product = ProductInventory.objects.get(product__slug = slug)
    deliveryoptions = Delivery.objects.filter(delivery_method = "HD")[:2]
    price = str(product.sale_price).replace('.', '')
    total = int(price)
    client_secret = get_client_secretkey(total, request.user.id)
    context = {
        'product': product,
        'client_secret': client_secret,
        "deliveryoptions": deliveryoptions
    }
    return render(request, 'payment/payment_oneclick.html', context)
# END GETTING IN ONE CLICK


