from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = "api"

urlpatterns = [
    # TOKEN
    path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name = 'token_verify'),
    # END TOKEN

    path('search/', views.search_list_api_view, name = 'search'),
    # _________ INVENTORY APP URLS _____________
    path('category/', views.categories_api_view, name = "category-list"),
    path('products_by_category/<slug:slug>/', views.products_api_view_by_category, name = 'products-by-category'),
    path('products_category_child/<slug:slug>/', views.products_api_view_by_category_child, name = "product-detail-by-categorychild"),
    path('product_detail/<slug:slug>/', views.product_detail_api_view, name = 'product-detail'),
    path('images/<int:id>/', views.media_images_api_view, name = 'media-images'),
    # _________ END INVENTORY APP URLS _____________

    # _________ ACCOUNT APP URLS _____________
    path('customers/', views.customers_api__get_view, name = 'customers'),
    path('customer/addresses/<int:id>/', views.addresses_api_get_view, name = 'customer-addresses'),
    path('customer/address_detail/<slug:id>/', views.address_api_get_view, name = 'address-detail'),
    # _________ END ACCOUNT APP URLS _____________

    # _________ CHECKOUT APP URLS _____________
    path('deliveries/', views.deliveries_api_view_get, name = 'delivery-list'),
    path('delivery_detail/<int:id>/', views.DeliveryRetrieveApiView.as_view(), name = 'delivery-detail'),
    # _________ END CHECKOUT APP URLS _____________
    
    # _________ ORDERS APP URLS _____________
    path('orders/<int:id>/', views.orders_api_view_get, name = 'orders'),
    path('order/<int:id>/', views.order_api_view_get, name = 'order-detail'),
    path('items/<int:id>/', views.orderitems_api_view_get, name = 'order-items'),
    path("item/<int:id>/", views.orderitem_api_view_get, name = 'item-detail'),

    # _________ END ORDERS APP URLS _____________
]