from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from inventory.models import (
    ProductInventory,
    Category,
    Product,
    Media,
    Brand,
    ProductAttributeValue
)
from account.models import Address, Customer
from checkout.models import Delivery
from orders.models import Order, OrderItem
from . import serializers
from . import client
# Create your views here.



    
# ________________ INVENTORY APP API ______________________


# SEARCH FOR PRODUCT INVENTORY TABLE 
# INCLUDED PRODUCT NAME BRAND NAME ALSO PRICE
@api_view(["GET"])
def search_list_api_view(request, *args, **kwargs):
    query = request.GET.get("q")
    if not query:
        return Response('ok :) :)', status=400)

    results = client.perform_search(query)
    return Response(results)
# END SEARCH


def get_views_url(request, endpoint):
    """
    THIS FUNCTION GIVES VIEWS URL PATH
    """
    url = reverse(endpoint)
    return request.build_absolute_uri(url)


def get_paginator(request, data, page_size = 10):
    """
    The function allows us to paginate a set of object's requests
    """
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(data, request)
    return paginator, result_page


def get_object_nums(obj):
    """
    The function gives us a number of object's queryset
    """
    return len(obj)


# GET CATEGORY API VIEW
@api_view(['GET'])
def categories_api_view(request):
    categories = Category.objects.prefetch_related("children").filter(parent = None)
    paginator, result_page = get_paginator(request, categories)
    serializer = serializers.CategorySerializers(result_page, many = True, context={'request': request})
    response = {
        'customers': get_views_url(request, "api:customers"),
        'delivery_companies': get_views_url(request, "api:delivery-list"),
        'categories':serializer.data
    }
    return paginator.get_paginated_response(response)
# END GET CATEGORY API VIEW


# GET PRODUCTS API VIEW FOR CATEGORY PRODUCT TABLE 
@api_view(['GET'])
def products_api_view_by_category(request, slug):
    category = get_object_or_404(Category.objects.prefetch_related('children'), slug=slug)
    products = Product.objects.prefetch_related("category__children").filter(category__in = category.children.all())
    serializer = serializers.ProductSerializer(products, many = True, context = {"request": request})
    return Response({"products": serializer.data, 'number_of_products': get_object_nums(products)})
# END GET PRODUCTS API VIEW FOR PRODUCT TABLE


#TOMENDE FUNCTION JOQARIDAG'I FUNCTION SAME YAGNIY BIRDEY OK :)
# GET PRODUCTS API VIEW BY CATEGORY'S CHILD
@api_view(['GET'])
def products_api_view_by_category_child(request, slug):
    products = Product.objects.filter(category__slug = slug)
    serializer = serializers.ProductSerializer(products, many = True, context = {"request": request})
    return Response({"products": serializer.data, "number_of_products": get_object_nums(products)})
# END GET PRODUCTS API VIEW BY CATEGORY'S CHILD


# GET PRODUCT INVENTORY TABLE FOR PRODUCT DETAIL
@api_view(['GET'])
def product_detail_api_view(request, slug):
    product = get_object_or_404(ProductInventory.objects.select_related("product", "brand"), product__slug = slug)
    serializer = serializers.ProductInventorySerializers(product, many = False, context={"request":request})
    return Response({"product detail": serializer.data})
# END GET PRODUCT INVENTORY TABLE FOR PRODUCT DETAIL


# GET MEDIA API VIEW IMAGES FOR PRODUCTS
@api_view(['GET'])
def media_images_api_view(request, id):
    images = Media.objects.select_related("product_inventory").filter(product_inventory__id = id)
    serializer = serializers.MediaSerializers(images, many = True)
    return Response({'images': serializer.data})
# END GET MEDIA API VIEW IMAGES FOR PRODUCTS



# ________________ END INVENTORY APP API ______________________



# ________________ ACCOUNT APP API ______________________

# CUSTOMER TABLE FOR CUSTOMERS API GET
@api_view(['GET'])
def customers_api__get_view(request):
    customers = Customer.objects.filter(is_staff = False)
    serializer = serializers.CustomerSerializers(customers, many = True, context = {"request":request})
    return Response({"customers": serializer.data, 'num_of_customers': get_object_nums(customers)})
# END CUSTOMER TABLE FOR CUSTOMERS API GET


# ADDRESS TABLE FOR ADDRESSES API GET
@api_view(['GET'])
def addresses_api_get_view(request, id):
    #addresses = Address.objects.select_related("customer").filter(customer__id = id)
    addresses = get_list_or_404(Address.objects.select_related('customer'), customer__id = id)
    serializer = serializers.AddressesSerializers(addresses, many = True, context = {"request": request})
    response = {
        "addresses": serializer.data
    }
    return Response(response)
# END ADDRESS TABLE FOR ADDRESSES API GET


# ADDRESS TABLE FOR ADDRESS DETAIL API GET
@api_view(['GET'])
def address_api_get_view(request, id):
    address = get_object_or_404(Address, id = id)
    serializer = serializers.AddressDetailSerializers(address, many = False)
    response = {
        "address_detail": serializer.data
    }
    return Response(response)
# END ADDRESS TABLE FOR ADDRESS DETAIL API GET

# ________________ END ACCOUNT APP API ______________________



# ________________ CHECKOUT APP API ______________________

# DELIVERY LIST API VIEW GET
@api_view(["GET"])
def deliveries_api_view_get(request):
    deliveries = Delivery.objects.all()
    serializer = serializers.DeliveryListSerializers(deliveries, many = True, context = {"request": request})
    response = {
        "deliveries": serializer.data,
        "num_of_deliveries": get_object_nums(deliveries)
    }
    return Response(response)
# END DELIVERY LIST API VIEW GET


# DELIVERY DETAIL API VIEW GET
class DeliveryRetrieveApiView(RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = serializers.DeliveryDetailSerializers
    lookup_field = "id"
# END DELIVERY DETAIL API VIEW GET

# ________________ END CHECKOUT APP API ______________________


# ________________ ORDERS APP API ______________________

# ORDERS API VIEW GET LIST
@api_view(['GET'])
def orders_api_view_get(request, id):
    orders = get_list_or_404(Order.objects.select_related("user"), user__id = id)
    serializer = serializers.OrderListSerializers(orders, many = True, context = {"request": request})
    response = {
        "orders": serializer.data,
        "num_of_orders": get_object_nums(orders)
    }
    return Response(response)
# END ORDERS API VIEW GET LIST


# ORDER API VIEW GET DETAIL
@api_view(['GET'])
def order_api_view_get(request, id):
    order = get_object_or_404(Order.objects.select_related("address", "user"), id = id)
    serializer = serializers.OrderDetailSerializers(order, many = False, context = {"request":request})
    response = {
        "order_detail": serializer.data
    }
    return Response(response)
# END ORDER API VIEW GET DETAIL


# ORDER ITEMS API VIEW GET LIST
@api_view(['GET'])
def orderitems_api_view_get(request, id):
    orderitems = get_list_or_404(OrderItem.objects.select_related("order", "product__product"), order__id = id)
    serializer = serializers.OrderItemListSerializers(orderitems, many = True, context = {"request": request})
    response = {
        "items": serializer.data,
        "num_of_items": get_object_nums(orderitems)
    }
    return Response(response)
# END ORDER ITEMS API VIEW GET LIST


# ORDER ITEM API VIEW GET DETAIL
@api_view(['GET'])
def orderitem_api_view_get(request, id):
    orderitem = get_object_or_404(OrderItem.objects.select_related("order", "product__product"), id = id)
    serializer = serializers.OrderItemDetailSerializers(orderitem, many = False)
    response = {
        "item_detail": serializer.data
    }
    return Response(response)
# END ORDER ITEM API VIEW GET DETAIL


# ________________ END ORDERS APP API ______________________

