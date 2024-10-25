# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home page showing list of products
    path('', views.home, name='home'),

    # Product detail page (example: /product/1/)
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/', views.products_list, name='products'),
    path('accout/', views.account, name='account'),

    # Checkout page (optional)
    path('checkout/', views.checkout, name='checkout'),

    # Order history page
    path('order-history/', views.order_history, name='order_history'),
]
