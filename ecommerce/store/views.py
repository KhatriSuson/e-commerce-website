# store/views.py

from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += 1
        order_item.save()
    else:
        # Handle anonymous user with session
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session['cart'] = cart

    return redirect('cart')