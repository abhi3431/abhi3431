from ast import Sub
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import *
from .models import Product,Cart,Order,Myorder
from django.db.models import Q 
import random
import razorpay 
from django.core.mail import send_mail

def index(request):
    return render(request, "index.html")


def base(request):
    return render(request, "base.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")

def product(request):
    context={}
    uid=request.user.id
    p=Product.objects.filter(is_active=True)
    context['prod']=p
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    context={}
    u= Product.objects.filter(q1 & q2)
    context['prod']=u
    print(u)
    return render(request,'index.html',context)

def sort_price(request,sv):
    if sv == "1":
        p=Product.objects.order_by('-price').filter(is_active=True)
        
    else:
        p=Product.objects.order_by('price').filter(is_active=True)
        
    context={}
    context['prod']=p
    return render(request,'index.html',context)

def filterbyprice(request):
    min=request.GET['min']
    max=request.GET['max']
    
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['prod']=p
    print(min,max)
    return render(request,'index.html',context)

def register(request):
    context = {}
    if request.method == "POST":
        uname = request.POST["uname"]
        upassword = request.POST["upass"]
        ucpassword = request.POST["ucom"]
        if uname == "" or upassword == "" or ucpassword == "":
            context["errmsg"] = "Field can not be Empty!!!"
            return render(request, "register.html", context)

        elif upassword != ucpassword:
            context["commsg"] = "INVALID PASSWORD...TRY AGAIN"
            return render(request, "register.html", context)

        else:
            try:
                u = User.objects.create(username=uname, email=uname, password=upassword)
                u.set_password(upassword)
                u.save()
                context["success"] = "registration successfully"
                return render(request, "register.html", context)
            except Exception:
                context["errmsg"] = "Username Already Exists"
                return render(request, "register.html", context)

    else:
        return render(request, "register.html", context)


def user_login(request):
    context = {}
    if request.method == "POST":
        usr = request.POST["uname"]
        pwd = request.POST["pass"]
        if usr == "" or pwd == "":
            context["errmsg"] = "Field cannot be empty"
            return render(request, "login.html", context)
        else:
            u = authenticate(username=usr, password=pwd)
            if u is not None:
                login(request, u)
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(request, "login.html", context)
    else:
        return render(request, "login.html")


def logout(request):
    logout(request)
    return redirect("/logout")


def place_order(request):
    return render(request, "placeorder.html")


def product_detail(request,pid):
    p = Product.objects.filter(id=pid)
    context={}
    context['prod'] = p
    return render(request, "product_detail.html",context)

def cart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        # print(u[0])
        # return HttpResponse("User Fetched")
        p = Product.objects.filter(id=pid)
        q1=Q(user_id=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['prod']=p
        if n>0:
            context['msg_alert']="Product already exists in the cart"
            print(n)
            return render(request,"product_detail.html",context)
        else:
            c=Cart.objects.create(user_id=u[0],pid=p[0])
            c.save()
            context['msg_success']="Product Successfully added to the cart"
            print(n)
            return render(request,"product_detail.html",context)
        
    else:
        return redirect("/login")
            
            
            
def view_cart(request):
    c=Cart.objects.filter(user_id=request.user.id)
    u = User.objects.filter(id= request.user.id)
    tot=0
    for x in c:
        tot=tot+x.pid.price*x.qty
    context={}
    context["prod"]=c
    context["tot"]=tot
    context['n']=len(c)
    context['name']=u[0].first_name + ' ' + u[0].last_name
    context['uname']=u[0].username
    return render(request,"cart.html",context)


def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')


def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect("/viewcart")


def placeorder(request):
    c=Cart.objects.filter(user_id=request.user.id)
    oid=random.randrange(1000,9999)
    for x in c:
        amount=x.pid.price*x.qty
        o=Order.objects.create(order_id=oid, user_id=x.user_id , pid=x.pid , qty=x.qty , amt=amount)
        o.save()
        x.delete()
         
    return redirect('/fetchorder')


def fetchorder(request):
    o=Order.objects.filter(user_id = request.user.id)
    u = User.objects.filter(id= request.user.id)
    # u.create(contact = 739)
    # u.update()
    tot=0
    for x in o:
        tot=tot+x.amt
    context={}
    context['prod']=o
    context['total']=tot
    context['n']=len(o)
    context['name']=u[0].first_name + ' ' + u[0].last_name
    context['uname']=u[0].username
    # context['contact']=u[0].contact
    return render(request,"placeorder.html",context)
    
    
def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_R7kWkFU6ZllnWF", "W0gE85soRmV6WanAQr1nW69n"))
    ord= Order.objects.filter(user_id=request.user.id)
    tot=0
    print(ord)
    for x in ord:
        tot = tot + x.amt 
        oid = x.order_id
    data = {"amount": tot , "currency": "INR" , "receipt": oid}
    payment = client.order.create(data = data)
    print(payment)
    context={}
    context['payment']=payment
    return render(request,"pay.html",context)

def paymentsuccess(request):
    sub = "Ekart Order Status"
    msg = 'Thanks for shopping !!'
    u = User.objects.filter(id = request.user.id)
    to = u[0]  # to fetch the emailid
    print(to)
    frm = "abhi7391940476@gmail.com"
    
    send_mail(
    sub,
    msg,
    frm,
    [to],
    fail_silently=False,
    )
    ord = Order.objects.filter(user_id = u[0])
    for x in ord:
        mo = Myorder.objects.create(order_id = x.order_id, 
                                    user_id = x.user_id,
                                    pid = x.pid,
                                    amt = x.amt, 
                                    qty = x.qty)
        mo.save()
        x.delete()
    return HttpResponse("payment sussessfully")
    
        
