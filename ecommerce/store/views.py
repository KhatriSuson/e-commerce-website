# store/views.py

from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required

def add_to_cart(request, product_id):
    # Get the product the user is adding to the cart
    product = Product.objects.get(id=product_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # If the user is authenticated, use their customer account
        customer = request.user.customer
        # Get or create an order for the user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # If the user is not authenticated, create a temporary cart using session data
        if 'order' not in request.session:
            request.session['order'] = {}
        
        # Retrieve the session order (temporary cart)
        order = request.session['order']
    
    # Add the product to the order (or cart)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    # You can set the quantity or other details here
    order_item.quantity += 1
    order_item.save()

    return redirect('cart')  # Redirect to cart page
