import random

import stripe
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from Online_Shop_fin import settings
from u_online_shop.models import Seller, Product, Category, Order
from .cart import Cart
from .forms import ProductForm, AddToCartForm, CheckoutForm
from .utilities import checkout


def homepage(request):
    newest_products = Product.objects.all()[0:7]

    return render(request, 'homepage.html', {'newest_products': newest_products})


def contact(request):
    return render(request, 'contact.html')


def become_seller(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            seller = Seller.objects.create(name=user.username, created_by=user)

            return redirect('homepage')

    else:
        form = UserCreationForm()

    return render(request, 'become_seller.html', {'form': form})


@login_required
def seller_admin(request):
    seller = Seller.objects.get(created_by=request.user)
    products = seller.products.all()
    orders = seller.orders.all()

    for order in orders:
        order.seller_amount = 0
        order.seller_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.seller == request.user.seller:
                if item.seller_paid:
                    order.seller_paid_amount += item.get_total_price()
                else:
                    order.seller_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'seller_admin.html', {'seller': seller, 'products': products, 'orders': orders})


@login_required
def edit_seller(request):
    seller = request.user.seller

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            seller.created_by.email = email
            seller.created_by.save()

            seller.name = name
            seller.save()

            return redirect('seller_admin')

    return render(request, 'edit_seller.html', {'seller': seller})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.slug = slugify(product.title)
            product.save()

        return redirect('seller_admin')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            return redirect('seller_admin')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def product(request, category_slug, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'Added to Cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    context = {
        'form': form,
        'product': product,
        'similar_products': similar_products,
    }

    return render(request, 'product.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'category.html', {'category': category})


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains(query)))

    return render(request, 'search.html', {'products': products, 'query': query})


def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']

                order = checkout(request, first_name, last_name, email, address, zipcode, phone,
                                 cart.get_total_cost())

                if order:  # If checkout was successful
                    cart.clear()
                    return redirect('success')
                else:
                    return redirect('cart')

    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})


def success(request):
    return render(request, 'success.html')


def sellers(request):
    sellers = Seller.objects.all()

    return render(request, 'sellers.html', {'sellers': sellers})


def seller(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)

    return render(request, 'seller.html', {'seller': seller})


@login_required
def view_orders(request):
    orders = Order.objects.filter(email=request.user.email)
    return render(request, 'view_orders.html', {'orders': orders})
