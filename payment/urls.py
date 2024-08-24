from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('orderplaced/', views.order_placed, name = 'order_placed'),
    path('webhook/', views.stripe_webhook),
    

    #GETTING IN ONE CLICK
    path('payment-one-click/<slug:slug>/', views.payment_one_click, name = 'payment-oneclick'),



]