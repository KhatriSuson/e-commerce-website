from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.models import User

# Home page displaying all products
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})
# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)

# View cart functionality for logged-in users
def view_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
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

# Add product to cart (both for logged-in and anonymous users)
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    messages.success(request, f'{product.name} was added to your cart.')
    return redirect('product_detail', product_id=product_id)

# View cart for session-based users
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
    return render(request, 'store/cart.html', context)

# Update cart item quantities
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
            messages.success(request, 'Cart updated successfully.')
        return redirect('view_cart')

# Remove item from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

# Placeholder for checkout functionality
def checkout(request):
    # Handle checkout process here
    pass

# View order history for authenticated users
def order_history(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer, complete=True)
        context = {'orders': orders}
        return render(request, 'store/order_history.html', context)
    else:
        return redirect('login')

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('account')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('account')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# User account dashboard
@login_required
def account(request):
    return render(request, 'accounts/account.html')

# User logout view
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')
