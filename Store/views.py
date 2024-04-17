from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from Store.forms.authforms import CustomerCreationForm, CustomerAuthForm
from Store.models import Tshirt, SizeVariant, Cart, Order, OrderItem, Payment, Occasion, Brand, Color, NeckType, Sleeve, IdealFor
from math import floor
from django.contrib.auth.decorators import login_required
from Store.forms.checkout_form import CheckForm
from instamojo_wrapper import Instamojo
from Tshop.settings import API_KEY, AUTH_TOKEN
API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
from django.db.models import Q

# Create your views here.
def index(request):
    query = request.GET
    # tshirts = []
    tshirts = Tshirt.objects.all().order_by('-id')

    brand = query.get('brand')
    color = query.get('color')
    necktype = query.get('necktype')
    idealfor = query.get('idealfor')
    sleeve = query.get('sleeve')
    occasion = query.get('occasion')

    # Filter based on query parameters
    filters = Q()  # Initialize an empty Q object to accumulate filters

    if brand:
        filters &=Q(brand__slug=brand)
    if color:
        filters &=Q(color__slug=color)
    if necktype:
        filters &=Q(neck_type__slug=necktype)
    if idealfor:
        filters &=Q(ideal_for__slug=idealfor)
    if sleeve:
        filters &=Q(sleeve__slug=sleeve)
    if occasion:
        filters &=Q(occasion__slug=occasion)

    tshirts = tshirts.filter(filters)
    # if brand!='' and brand is not None:
    #     tshirts = tshirts.filter(brand__slug=brand)
    # if color!='' and color is not None:
    #     tshirts = tshirts.filter(color__slug=color)
    # if necktype!='' and necktype is not None:
    #     tshirts = tshirts.filter(neck_type__slug=necktype)
    # if idealfor!='' and idealfor is not None:
    #     tshirts = tshirts.filter(ideal_for__slug=idealfor)
    # if sleeve!='' and sleeve is not None:
    #     tshirts = tshirts.filter(sleeve__slug=sleeve)
    # if occasion!='' and occasion is not None:
    #     tshirts = tshirts.filter(occasion__slug=occasion)
    #access Filter Data
    occasions = Occasion.objects.all()
    colors = Color.objects.all()
    brands = Brand.objects.all()
    sleeves = Sleeve.objects.all()
    idealfors = IdealFor.objects.all()
    necktypes = NeckType.objects.all()

    # tshirts = Tshirt.objects.all()
    cart = request.session.get('cart')
    # for tsh in tshirts:
    #     min_price = tsh.sizevariant_set.all().order_by().first()
    #     tsh.min_price = min_price.price
    #     tsh.after_discount = tsh.min_price - (tsh.discount/100)
    #     tsh.after_discount = floor(tsh.after_discount)

    context = {
        'tshirts':tshirts,
        'occasions':occasions,
        'brands':brands,
        'colors':colors,
        'necktypes':necktypes,
        'sleeves':sleeves,
        'idealfors':idealfors
    }
    return render(request, template_name='store/index.html',context=context)

def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    
    for c in cart:
        tshirt_id = c.get('tshirt')
        tshirt  = Tshirt.objects.get(pk=tshirt_id)
        c['size'] = SizeVariant.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt'] = tshirt

    context = {
        'cart':cart
    }
    return render(request, template_name='store/cart.html',context=context)

@login_required(login_url='login')
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-date').exclude(order_status="PENDING")
    context = {
        'orders':orders
    }
    return render(request, template_name='store/orders.html', context=context)

def login(request):
    if (request.method == 'GET'):
        form = CustomerAuthForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page
        context = {
            'form':form
        }
        return render(request, template_name='store/login.html', context=context)
    else:
        form = CustomerAuthForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user:
                loginuser(request,user)
                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantity = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizeVariant = SizeVariant.objects.get(size=size,tshirt=tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()

                cart = Cart.objects.filter(user=user)
                session_cart = []
                for c in cart:
                    obj = {
                        'size': c.sizeVariant.size,
                        'tshirt': c.sizeVariant.tshirt.id,
                        'quantity': c.quantity
                    }
                    session_cart.append(obj)
                request.session['cart'] = session_cart
                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = 'index'
                return redirect(next_page)
        else:
            context = {
            'form':form
            }
    return render(request, template_name='store/login.html', context=context)


def logout(request):
    # request.session.clear()
    logoutuser(request)
    return redirect('login')

def signup(request):
    if (request.method == 'GET'):
        form = CustomerCreationForm()
        context = {
            'form':form
        }
        return render(request, template_name='store/signup.html', context=context)
    else:
        form =CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            form.save()

            return redirect('login')
        else:
            context = {
            'form':form
        }
        return render(request, template_name='store/signup.html', context=context)
    
def show_products(request,id):
    tshirt = Tshirt.objects.get(pk=id)
    tsize = request.GET.get('size')
    if tsize==None:
        tsize = tshirt.sizevariant_set.all().order_by('price').first()
    else:
        tsize = tshirt.sizevariant_set.get(size=tsize)
    size_price = floor(tsize.price)
    sell_price = floor(size_price - (size_price*(tshirt.discount/100)))
    context = {
        'tshirt':tshirt,
        'price':size_price,
        'sell_price':sell_price,
        'active_size':tsize
    }
    return render(request, template_name='store/products.html', context=context)

def add_to_cart(request,id,size):
    user = None
    if request.user.is_authenticated:
        user = request.user

    cart = request.session.get('cart')
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(id=id)
    size_temp = SizeVariant.objects.get(size=size,tshirt=tshirt)
    
    flag = True
    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')
        size_short = cart_obj.get('size')
        if t_id == id and size_short == size:
            flag = False
            cart_obj['quantity'] += 1

    if flag:
        cart_obj = {
            'tshirt':id,
            'size':size,
            'quantity':1
        }
        cart.append(cart_obj)

    if user is not None:
        existing = Cart.objects.filter(user=user, sizeVariant=size_temp)

        if len(existing)>0:
            obj = existing[0]
            obj.quantity += 1
            obj.save()
        else:
            c = Cart()
            c.user = user
            c.sizeVariant = size_temp
            c.quantity = 1
            c.save()
    
    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)

# Utility
def cart_payable_amount(cart):
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        sale_price = floor(price - (price * (discount/100)))
        total_of_single_product = sale_price * c.get('quantity')
        total += total_of_single_product
    return total

@login_required(login_url='login')
def checkout(request):
   if request.method == 'GET':
        form = CheckForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []
    
        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj = SizeVariant.objects.get(size=size_str,tshirt=tshirt_id)
            c['size'] = size_obj
            c['tshirt'] = size_obj.tshirt

        context = {
            'form':form,
            'cart':cart
        }
        return render(request,template_name='store/checkout.html',context=context)
   else:
       form = CheckForm(request.POST)
       user = None
       if request.user.is_authenticated:
           user = request.user
       if form.is_valid():
           cart = request.session.get('cart')
           if cart is None:
               cart = []
           for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj = SizeVariant.objects.get(size=size_str,tshirt=tshirt_id)
                c['size'] = size_obj
                c['tshirt'] = size_obj.tshirt
           shipping_address = form.cleaned_data.get('shippping_address')
           phone = form.cleaned_data.get('phone')
           payment_method = form.cleaned_data.get('payment_method')
           total = cart_payable_amount(cart)
           print(shipping_address,phone,payment_method,total)
           order = Order()
           order.shippping_address = shipping_address
           order.phone = phone
           order.payment_method = payment_method
           order.order_status = 'PENDING'
           order.user = user
           order.total = total
           order.save()

           # Saving Order Item
           for c in cart:
               order_item = OrderItem()
               order_item.order = order
               size = c.get('size')
               tshirt = c.get('tshirt')
               order_item.price = floor(size.price - (size.price*(tshirt.discount/100)))
               order_item.quantity = c.get('quantity')
               order_item.size = size
               order_item.tshirt = tshirt
               order_item.save()
            
           # Creating Payment
           response = API.payment_request_create(
                amount=order.total,
                purpose='Payment for Tshirts',
                send_email=True,
                buyer_name=f'{user.first_name} {user.last_name}',
                email=user.email,
                redirect_url="http://localhost:8000/validate_payment"
            )
           payment_request_id = response['payment_request']['id']
           url = response['payment_request']['longurl']

           payment = Payment()
           payment.order = order
           payment.payment_request_id = payment_request_id
           payment.save()

            
           return redirect(url)
       else:
           return redirect('/checkout')
       
def validate_payment(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    response = API.payment_request_payment_status(payment_request_id,payment_id)
    # status = response['payment_request']['payment']['status']    
    status = response.get('payment_request').get('payment').get('status')   

    if status != 'Failed':
        try:
            payment = Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = 'PLACED'
            order.save()

            # Delete Cart from session
            cart = []
            request.session['cart'] = cart

            # Delete Cart from database
            Cart.objects.filter(user=user).delete()

            return redirect('orders')
        except:
            return render(request, template_name='store/payment_failed.html')
    else:
        return render(request, template_name='store/payment_failed.html')
    # return HttpResponse(status)