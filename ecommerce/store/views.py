# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Customer
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)

def view_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # Handle anonymous user with session-based cart (see earlier explanation)
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

# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#         order_item.quantity += 1
#         order_item.save()
#     else:
#         cart = request.session.get('cart', {})
#         if product_id in cart:
#             cart[product_id] += 1
#         else:
#             cart[product_id] = 1
#         request.session['cart'] = cart
    
#     return redirect('cart')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'name': product.name, 'price': product.price, 'quantity': 1}

    request.session['cart'] = cart
    messages.success(request, f'{product.name} was added to your cart.')
    return redirect('product_detail', product_id=product_id)

def remove_from_cart(request, product_id):
    # Similar to add_to_cart, but for removing products from the cart
    pass

def checkout(request):
    # Handle checkout process here
    pass

def order_history(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer, complete=True)
        context = {'orders': orders}
        return render(request, 'store/order_history.html', context)
    else:
        return redirect('login')
