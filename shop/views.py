from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from shop.models import *
import random
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'home.html', context)

def description(request, id):
    product = Product.objects.get(id = id)
    context = {"product": product}
    return render(request, "products/description.html", context)

def addcart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST["product_id"])
            prod_qty = int(request.POST["product_qty"])
            if Cart.objects.filter(user = request.user, product_id = prod_id).exists():
                if Cart.objects.filter(user = request.user, product_id = prod_id, quantity = prod_qty).exists():
                    return HttpResponse( 'Product is alreday in cart')
                else:
                    product_cart = Cart.objects.get(user = request.user, product_id = prod_id)
                    product_cart.quantity = prod_qty
                    product_cart.save()
                    return HttpResponse("Quantity updated")
            else:
                Cart.objects.create(user = request.user, product_id = prod_id, quantity = prod_qty)
                return HttpResponse("Product added successfully")
        else:
            return HttpResponse( 'Please login to continue')
    return redirect("/")

def cartview(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        total = 0
        for item in cart:
            total += item.quantity * item.product.selling_price

        context = {"cart":cart,
                   "total": total}
        print(total)
        return render(request, "cart/cartview.html", context)
    else:
        messages.info(request, "Login to Continue")

def deleteitem(request):
    if request.method == "POST":
        prod_id = int(request.POST["prod_id"])
        item = Cart.objects.get(user= request.user, product_id = prod_id)
        item.delete()
        return HttpResponse("item deleted successfully")
    
    return redirect("/")

def checkout(request):
    cart = Cart.objects.filter(user = request.user)
    total = 0
    for item in cart:
        total = item.product.selling_price * item.quantity

    context = {"total": total}
    return render(request, 'checkout/checkout.html', context)

def placeorder(request):
    if request.method == "POST":
        neworder = Order()
        neworder.user = request.user
        neworder.first_name = request.POST["first_name"]
        neworder.last_name = request.POST["last_name"]
        neworder.city = request.POST["city"]
        neworder.email = request.POST["email"]
        neworder.address = request.POST["address"]
        neworder.zipcode = request.POST["zip"]
        neworder.payment_mode = request.POST["payment_mode"]

        cart = Cart.objects.filter(user = request.user)
        total = 0
        for item in cart:
            total = item.product.selling_price * item.quantity
        neworder.total = total

        trackingno = "mohssine"+str(random.randint(111111, 999999))
        while Order.objects.filter(tracking_no = trackingno) is None:
            trackingno = "mohssine"+str(random.randint(111111, 999999))
        neworder.tracking_no = trackingno
        neworder.save()

        orderitems = Cart.objects.filter(user = request.user)
        for item in orderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                quantity = item.quantity,
                price = item.product.selling_price
            )

        Cart.objects.filter(user = request.user).delete()
        messages.success(request, 'Order placed successfully')
    return redirect("/")

def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["password1"] 
        if password1 == password2:
            if User.objects.filter(email = email).exists():
                messages.warning(request, "this email is already exists!")
                return redirect("register")
            elif User.objects.filter(username = name).exists():
                messages.warning(request, "this name is already exists!")
                return redirect("register")
            else:
                newuser = User.objects.create_user(username=name, email=email, password= password1)
                newuser.save()
                return redirect("login")

        else:
            messages.warning(request, 'the two passwords dont match')
            return redirect("register")
    return render(request, 'accounts/register.html')

def loginpage(request):
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]
        user = auth.authenticate(username = name, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.warning(request, "invalid data")
            return redirect("login")
    return render(request, "accounts/login.html")

def logOut(request):
    auth.logout(request)
    return redirect("/")

def search(request):
    if request.method == "POST":
        val = request.POST["search_val"]
        products = Product.objects.filter(name__contains = val)
        context = {"products":products}
        return render(request, 'search/search.html', context)
    
    else:
        return render(request, 'search/search.html')
    
def getproducts(request):
    products = Product.objects.all()
    return JsonResponse({"products":list(products.values())})

def dashboard(request):
    customer = Customer.objects.filter(user=request.user)
    context = {"customer": customer}
    return render(request, 'dashboard/dashboard.html', context)

def editprofile(request):
    # try:
    #     customer = Customer.objects.filter(user=request.user)
    # except Customer.DoesNotExist:
    #     customer = Customer()
    customer = Customer.objects.filter(user=request.user)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        profile_pic = request.POST["profile_pic"]
        caption = request.POST["caption"]
        newcustomer = Customer()
        newcustomer.user = request.user
        newcustomer.first_name = first_name
        newcustomer.last_name = last_name
        newcustomer.image = profile_pic
        newcustomer.caption = caption
        newcustomer.save()
        return redirect("dashboard")
    context = {"customer": customer}
    return render(request, "dashboard/editprofile.html", context)