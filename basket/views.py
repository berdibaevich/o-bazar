from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from inventory.models import ProductInventory
from .basket import Basket
from checkout.models import Delivery
# Create your views here.


# BASKET LIST
def basket_list(request):
    return render(request, 'basket/list.html')
# END BASKET LIST


#ADD BASKET VIEWS
def add_basket(request):
    """
    Add button this function of role is Grab product info 
    using Ajax and response JsonResponse
    """
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        quantity = int(request.POST.get('product_quantity'))
        product_id = int(request.POST.get('product_id'))
        product_inventory = get_object_or_404(ProductInventory, pk = product_id)
        basket.add(product_inventory, quantity)

        total_quantity = basket.__len__()

        response = JsonResponse({'total_qty': total_quantity})
        return response
#END ADD BASKET VIEWS


#UPDATE BASKET VIEWS
def update_basket(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_quantity = int(request.POST.get('product_quantity'))
        product_id = request.POST.get('product_id')
        basket.update_basket(product_id, product_quantity)
        total_qty = basket.__len__()
        total_price = basket.get_total_price()

        response = JsonResponse({'total_price':total_price, 'total_qty': total_qty})
        return response


#DELETE BASKET VIEWS
def delete_basket(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        basket.remove(product_id)
        total_qty = basket.__len__()
        total_price = basket.get_total_price()

        response = JsonResponse({'total_price': total_price, 'total_qty': total_qty})
        return response
#END DELETE BASKET VIEWS
    

# DELIVERY CHANGE OPTIONS RADIO
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        delivery_id = int(request.POST.get("deliveryoption"))
        delivery = get_object_or_404(Delivery, pk = delivery_id)
        total_price = basket.basket_update_delivery(delivery_price=delivery.delivery_price)

        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {
                'delivery_id': delivery.id
            }
        else:
            session['purchase']['delivery_id'] = delivery.id
            session.modified = True

        response = JsonResponse({
            "total": total_price,
            "delivery_price": delivery.delivery_price
        })
        return response
# END DELIVERY CHANGE OPTIONS RADIO


