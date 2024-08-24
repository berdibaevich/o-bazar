from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('deliverychoices/', views.deliverychoices, name = 'deliverychoices'),
    path('delivery_address/', views.delivery_address, name = 'delivery_address'),
    path('pay/', views.pay_securely, name = 'pay'),




]