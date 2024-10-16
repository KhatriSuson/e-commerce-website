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

# store/views.py

def view_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # Use session-based cart for anonymous users
        cart = request.session.get('cart', {})
        items = []
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            item = {
                'product': product,
                'quantity': quantity,
                'get_total': product.price * quantity,
            }
            items.append(item)

    context = {'items': items}
    return render(request, 'store/cart.html', context)


#Alternatively, if you want to ensure that only authenticated users can add items to the cart, you can use Django's @login_required decorator:
# @login_required
# def add_to_cart(request, product_id):
#     customer = request.user.customer
#     product = Product.objects.get(id=product_id)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#     order_item.quantity += 1
#     order_item.save()
#     return redirect('cart')