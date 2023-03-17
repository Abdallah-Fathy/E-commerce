import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total':0, "get_cart_items":0, 'shipping':False}
    cartItem = order['get_cart_items']

    for i in cart:
        try:
            cartItem += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name' :product.name,
                    'price' :product.price,
                    'imageURL' :product.imageURL,
                    },
                'quantity' : cart[i]["quantity"],
                'get_total' :total
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItem, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.custromer
        order, created = Order.objects.get_or_create(custromer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cookiData = cookieCart(request)
        cartItem = cookiData['cartItems']
        order = cookiData['order']
        items = cookiData['items']
    return {'cartItems':cartItem, 'order':order, 'items':items}

def guestOrder(request, data):
    print('User is not logged in..')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Custromer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order