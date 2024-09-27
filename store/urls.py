from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='home'),
    path('products', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('accounts/signup/', register, name='account_signup'),
    path('accounts/login/', CustomLoginView, name='account_login'),
    path('accounts/logout/', custom_logout, name='account_logout'),
    path('accounts/setting/', account_setting, name='account_setting'),
    
    path('about_us/', about, name='about'),
    path('contact/', contact, name='contact'),
    
]