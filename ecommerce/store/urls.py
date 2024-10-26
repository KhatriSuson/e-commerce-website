from django.urls import path
from .views import (
    home,
    product_list,
    product_detail,
    view_cart,
    add_to_cart,
    update_cart,
    remove_from_cart,
    checkout,
    order_history,
    register,
    user_login,
    account,
    user_logout,
)

urlpatterns = [
    path('', home, name='home'),
    # path('products/', product_list, name='product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-history/', order_history, name='order_history'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('account/', account, name='account'),
    path('logout/', user_logout, name='logout'),
]
