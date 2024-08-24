from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView
from .forms import (
    UserLoginForm,

)

app_name = 'account'


urlpatterns = [
    path('sign-up/', views.account_register, name = 'register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name = 'activate'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('edit-profile/', views.edit_profile, name = 'edit-account'),

    # LOGIN & LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name = "account/login.html",
    form_class = UserLoginForm), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/'), name = 'logout'),
    # END LOGIN & LOGOUT

    #DELETE ACCOUNT
    path('profile/delete_account/', views.delete_account, name = 'delete-account'),
    path('profile/delete-confirm/', TemplateView.as_view(template_name = 'account/delete_account.html'), name = 'delete_confirmation'),
    
    # addresses
    path('addresses/', views.view_address, name = 'addresses'),
    path('add/', views.add_address, name = 'add-address'),
    path('edit/<slug:id>/', views.edit_address, name = 'edit-address'),
    path('delete/<slug:id>/', views.delete_address, name = 'delete-address'),
    path('set_default/<slug:id>/', views.set_default, name = 'set-default'),

    path('api_page/', views.get_api_page, name = 'api-page'),

    
]