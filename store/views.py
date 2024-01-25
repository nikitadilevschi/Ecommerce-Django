import datetime
import json
import time

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .utils import cookieCart, cartData, guestOrder


# Create your views here.

def store(request):
    selected_category_id = request.GET.get('category', '0')  # Set the default value to '0' if not provided
    if selected_category_id == '0':
        products = Product.objects.all()  # If '0' is selected, fetch all products
    else:
        products = Product.objects.filter(category=selected_category_id)

    context = {
        'products': products,
        'cartItems': cartData(request)['cartItems'],
        'selected_category_id': selected_category_id,

    }

    return render(request, 'store/store.html', context)


def cart(request):
    context = cartData(request)
    return render(request, 'store/cart.html', context)


def product_detail(request, product_id):

    products = Product.objects.all()
    product = Product.objects.get(id=product_id)

    context = {'product': product, 'products': products, 'current_product': product,
               'cartItems': cartData(request)['cartItems']}

    return render(request, 'store/product_detail.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    start_time = time.time()
    for item in items:
        if not cartItems:
            return redirect('store')
    context = {'order': order,'categories': categories, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)





def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request,data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete', safe=False)