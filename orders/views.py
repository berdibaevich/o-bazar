from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import Address
from basket.basket import Basket
from .models import OrderItem, Order
from inventory.models import ProductInventory, BestSellingProducts


# Create your views here.


# USER'S ORDERS
@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.select_related("address").filter(user_id = user_id).filter(billing_status=True)
    context = {
        'orders': orders
    }
    return render(request, 'orders/orders.html', context)
# END USER'S ORDERS


# GET ADDRESS ID FROM SESSION
def get_address_id_from_session(request):
    address_id = request.session.get("address")['address_id']
    return address_id
# END GET ADDRESS ID FROM SESSION


# CREATE ORDER FUNCTION
def create_order(address_id, order_key, user, total_paid):
    if Order.objects.filter(order_key = order_key).exists():
        pass
    else:
        order = Order.objects.create(
            user = user,
            address_id = address_id,
            total_paid = total_paid,
            order_key = order_key,
            billing_status = True
        )
        return order.pk
# END CREATE ORDER FUNCTION



# CREATE ORDERITEM FUNCTION
def create_orderitem(request, order_id):
    basket = Basket(request)
    for item in basket:
        product = item.get('product')
        quantity = item['quantity']
        OrderItem.objects.create(
            order_id = order_id,
            product = product,
            price = item['price'],
            quantity = quantity
        )
        add_to_best_selling_products(product=product, quantity=quantity)
# END CREATE ORDERITEM FUNCTION


# ADD
def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        user = request.user
        order_key = request.POST.get('order_key')
        baskettotal = basket.get_total_and_delivery_price()
        address_id = get_address_id_from_session(request)

        order_id = create_order(address_id=address_id, order_key=order_key, user=user, total_paid=baskettotal)
        orderitem = create_orderitem(request, order_id)          
        response = JsonResponse({'success': True})
        return response
# END ADD


# PAYMENT CONFIRMATION
def payment_confirmation(data):
    Order.objects.filter(order_key = data).update(billing_status = True)
# END PAYMENT CONFIRMATION





# BELLOW GET IN ONE CLICK PROCCESS

# CHECK ADDRESS
def check_address(user):
    address = Address.objects.filter(customer = user, default = True).exists()
    if address:
        Address.objects.filter(customer = user, default = True).update(default = False)
# END CHECK ADDRESS

# CREATE ADDRESS
def create_address(request, user):
    phoneNumber = request.POST.get('phoneNumber')
    fio = request.POST.get('fio')
    address1 = request.POST.get('address1')
    address2 = request.POST.get('address2')
    country = request.POST.get('country')
    postCode = request.POST.get('postCode')

    # CHECKING PROCCESS IF ADDRESS HAS DEFAULT TRUE UPDATED TO FALSE
    check_address(user)

    address = Address.objects.create(
        customer = user,
        full_name = fio,
        phone = phoneNumber,
        postcode = postCode,
        address_line = address1, 
        address_line2 = address2,
        town_city = country,
        default = True
    )
    return address.id
# END CREATE ADDRESS


# CREATE ORDER
def create_order_and_get_id(user_id, address_id, order_key, total_paid):
    if Order.objects.filter(order_key = order_key).exists():
        pass
    else:
        order = Order.objects.create(
            user_id = user_id,
            address_id = address_id,
            total_paid = total_paid,
            order_key = order_key,
            billing_status = True
        )
        return order.pk
# END CREATE ORDER


# CREATE ORDERITEM
def create_order_item(order_id, product_id, price, quantity = 1):
    OrderItem.objects.create(
        order_id = order_id,
        product_id = product_id,
        price = price,
        quantity = quantity
    )
# END CREATE ORDERITEM


# ADD TO BEST SELLING PRODUCT
def add_to_best_selling_products(product, quantity = 1):
    best_selling = BestSellingProducts.objects.filter(product=product).first()
    if best_selling:
        best_selling.quantity += quantity
        best_selling.save()
    else:
        BestSellingProducts.objects.create(product = product, quantity = quantity)
# END ADD TO BEST SELLING PRODUCT



# ADD PAYMENT ONE CLICK
def add_one_click(request):
    if request.POST.get('action') == 'post':
        user = request.user
        order_key = request.POST.get('order_key')
        product_id = request.POST.get('product_id')
        total_price = request.POST.get("total_price")
        product = get_object_or_404(ProductInventory, pk = product_id)
        address_id = create_address(request, user)
        order_id = create_order_and_get_id(user.pk, address_id, order_key, total_paid=total_price)
        order_item = create_order_item(order_id, product_id, product.sale_price)
        add_to_best_selling_products(product=product)
        response = JsonResponse({'success': True})
        return response
# END ADD PAYMENT ONE CLICK







