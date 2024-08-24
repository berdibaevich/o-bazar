from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from checkout.models import Delivery
from .models import (
    Product,
    ProductInventory,
    Category,
    Media,
    BestSellingProducts
)


# FOR GIFTS IMPORT
from django.conf import settings
from .floweraura_category import GiftCategory
from .floweraura_product import GiftProduct
# END FOR GIFTS IMPORT

# FOR PRACTISE BUT IMAGES DOESNT WORK
def get_fake(request):
    products = Media.objects.select_related("product_inventory__product").filter(is_feature = True).values(
        "image", "alt_text","product_inventory__sale_price", "product_inventory__product__id", "product_inventory__product__name", "product_inventory__product__slug"
    )
    context = {
        "products": products
    }
    return render(request, 'inventory/fake.html', context)
# 


# Create your views here.

# 404 PAGE
def handler404(request, exception):
    return render(request, '404.html', status=404)
# END 404 PAGE

# 500 SERVER ERROR
def server_error(request):
    return render(request, '500.html', status=500)
# END 500 SERVER ERROR



# SEARCH FUNCTION
def search(q = None):
    query = (
        Q(product__name__icontains = q) |
        Q(brand__name__icontains = q) |
        Q(sale_price__icontains = q)
    )
    datas = ProductInventory.objects.filter(query).select_related("product")

    if len(datas) == 0:
        return 0
    return datas
# END SEARCH FUNCTION

# ALL PRODUCTS
def products(request):
    q = request.GET.get('q') or None
    if q == None:
        products = ProductInventory.objects.select_related("product")
    else:
        products = search(q)
        if products == 0:
            messages.warning(request, 'Product does not exists!')
            return redirect('inventory:list-products')
    context = {
        'products': products
    }
    return render(request, 'inventory/products.html', context)
# END ALL PRODUCTS


# BEST SELLING PRODUCTS
def get_best_selling_products(request):
    products = BestSellingProducts.objects.select_related("product").filter(quantity__gt = 1)
    context = {
        "products": products
    }
    return render(request, 'inventory/best_selling_products.html', context)
# END BEST SELLING PRODUCTS


# PRODUCTS BY CATEGORY
def products_by_category(request, slug):
    #slug = "biznes-kitaplar"
    category = get_object_or_404(Category, slug = slug) 
    products = ProductInventory.objects.filter(
        product__category__in = Category.objects.get(slug=slug).get_descendants(include_self = True)
    )
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'inventory/products_by_category.html', context)
# END PRODUCTS BY CATEGORY


# PRODUCT BY CATEGORY CHILDREN
def products_by_category_children(request, slug):
    category = get_object_or_404(Category, slug = slug)
    products = ProductInventory.objects.filter(
        product__category__in = Category.objects.get(slug=slug).get_descendants(include_self = True)
    )
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'inventory/filtered_category_for_products.html', context)
# END PRODUCT BY CATEGORY CHILDREN


# PRODUCT DETAIL
def product_detail(request, slug):
    product = get_object_or_404(ProductInventory.objects.select_related("product", "brand"), product__slug = slug)
    context = {
        'product': product
    }
    return render(request, 'inventory/product_detail.html', context)
# END PRODUCT DETAIL





# GIFT IDEAS

def get_data_from_floweraura(url):
    data = GiftCategory(url=url)
    return data


def get_gifts(num: int):
    url = settings.FLOWERAURA_URL
    data = get_data_from_floweraura(url)
    return data.filter_gift(num)



def get_gifts_list(request):
    context = {
        "gifts_hampers": get_gifts(0),
        "for_hers": get_gifts(1),
        "for_hims": get_gifts(2),
        "home_kitchens": get_gifts(3),
        "fashions": get_gifts(4),
        "more_gifts": get_gifts(5),
    }
    return render(request, 'inventory/gifts.html', context)


def check_name(name: str):
    arr = ['Girlfriend', 'Wife', 'Mother', 'Sister', 'Daughter', 'Boyfriend', 'Husband', 'Father', 'Brother', 'Son', 'Boys', "Kids", "Parents"]
    if name not in arr:
        return name
    return f"For {name}"


def get_products_by_gift(request, name):
    url = settings.FLOWERAURA_URL
    products = GiftProduct(url)
    checked_name = check_name(name)
    context = {
        'gift': name,
        'products': products.get_products(checked_name),
    }
    return render(request, 'inventory/products_by_gift.html', context)


# END GIFT IDEAS


# DELIVERY SERVICE
def get_delivery_services(request):
    deliveries = Delivery.objects.all()
    page = "delivery"
    context = {
        "deliveries": deliveries,
        "page":page
    }
    return render(request, 'inventory/delivery_services.html', context)



def get_delivery_method(request, method):
    deliveries = Delivery.objects.filter(delivery_method = method)
    page = "method"
    context = {
        "deliveries": deliveries,
        "page":page
    }
    return render(request, 'inventory/delivery_services.html', context)


# END DELIVERY SERVICE