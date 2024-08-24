from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('add/', views.add, name = 'add'),
    path('orders/', views.user_orders, name = 'order-list'),
    
    # ADD ONE CLICK
    path('add-one-click/', views.add_one_click, name = 'add-one-click'),
    



]