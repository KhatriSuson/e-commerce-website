from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ShoppingCart

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def cart(request):
    return render(request, 'store/cart.html')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = ShoppingCart.objects.get_or_create(customer=request.user.customer)
    cart.product.add(product)
    return redirect('cart')