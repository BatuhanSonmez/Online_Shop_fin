# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from django.contrib import messages
from .cart import Cart
from .models import Order, OrderItem, Product

def checkout(request, first_name, last_name, email, address, zipcode, phone, amount):
    # Check inventory before creating the order
    for item in Cart(request):
        product = item['product']
        if product.quantity < item['quantity']:
            messages.error(request, f"The item '{product.title}' is out of stock.")
            return None  # Abort checkout process

    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address,
                                 zipcode=zipcode, phone=phone, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], seller=item['product'].seller,
                                 price=item['product'].price, quantity=item['quantity'])

        # Reduce the product inventory
        product.quantity -= item['quantity']
        product.save()

        order.sellers.add(item['product'].seller)

    return order
