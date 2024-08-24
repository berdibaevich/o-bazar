from django.urls import path
from . import views

app_name = "wishlist"


urlpatterns = [
    path('list/', views.get_wishlist, name = 'list'),
    path('add/', views.add, name = 'add'),
    path('remove/', views.remove, name = 'remove'),
    



]