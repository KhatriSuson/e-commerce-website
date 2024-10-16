# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Home page showing list of products
    path('', views.home, name='home'),

    # Product detail page (example: /product/1/)
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart page (showing items in the cart)
    path('cart/', views.view_cart, name='cart'),

    # Add a product to the cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Remove item from the cart (optional)
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout page (optional)
    path('checkout/', views.checkout, name='checkout'),

    # Order history page
    path('order-history/', views.order_history, name='order_history'),
]
