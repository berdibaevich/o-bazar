from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_list, name = 'list'),
    path('add/', views.add_basket, name = 'add_to_basket'),
    path('update/', views.update_basket, name = 'update_basket'),
    path('remove/', views.delete_basket, name = 'delete_basket'),
    #DELIVERY OPTIONS
    path('udpate_delivery/', views.basket_update_delivery, name = "basket-update-delivery"),


]
