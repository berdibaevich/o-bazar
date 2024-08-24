from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from inventory.models import ProductInventory
from django.contrib import messages
from .wishlist import WishList

# Create your views here.

# WISHLIST ADD
def add(request):
    wishlist = WishList(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(ProductInventory, pk = product_id)
        wishlist.add(product.pk)
        how_many_wishlist = wishlist.__len__()
        message = wishlist.get_message()
        
        if message:
            messages.success(request, f'{product.product.name} added to your wishlist.')
        else:
            messages.info(request, f"{product.product.name} removed from your wishlist.")

        response = JsonResponse({'how_many': how_many_wishlist})
        return response
# END WISHLIST ADD 

# MY WISHLIST
def get_wishlist(request):
    return render(request, 'wishlist/list.html')
# END MY WISHLIST


# REMOVE WISHLIST
def remove(request):
    wishlist = WishList(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        wishlist.remove(product_id=product_id)
        how_many = wishlist.__len__()
        response = JsonResponse({'how_many': how_many})
        return response
# END REMOVE WISHLIST
