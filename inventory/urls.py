from django.urls import path
from django.conf.urls import handler404, handler500
from . import views

app_name = 'inventory'



urlpatterns = [
    path('', views.products, name = 'list-products'),
    path('best_selling/', views.get_best_selling_products, name = 'best-products'),
    path('list/', views.get_fake),
    path('products/<slug:slug>/', views.products_by_category, name = 'products-by-category'),
    path('product_detail/<slug:slug>/', views.product_detail, name = 'product-detail'),
    path('category-child/<slug:slug>/', views.products_by_category_children, name = 'category-child'),
    path('gifts/', views.get_gifts_list, name = 'gifts'),
    path('products_by_gift/<str:name>/', views.get_products_by_gift, name = 'products-by-gifts'),
    path('delivery_services/', views.get_delivery_services, name = 'delivery-services'),
    path('delivery_services/<str:method>/', views.get_delivery_method, name = 'delivery_services-method')
]
handler404 = 'inventory.views.handler404'
handler500 = 'inventory.views.server_error'