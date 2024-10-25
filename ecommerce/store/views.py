# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Customer
from django.contrib import messages
from decimal import Decimal

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
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),  # Convert Decimal to float here
            'quantity': 1
        }

    request.session['cart'] = cart
    messages.success(request, f'{product.name} was added to your cart.')
    return redirect('product_detail', product_id=product_id)

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    total_price = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        total_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
            messages.success(request, 'Cart updated successfully.')
        return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


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
