from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.

@unauthenticated_user
def registerUser(request):
    #if request.user.is_authenticated:
        #return redirect("home")
    #else:
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #group = Group.objects.get(name='customer')
            #user.groups.add(group)
            #Customer.objects.create(user=user, name=username)
            messages.success(request, "Account created successfully for "+ username)
            return redirect("login")
    context = {'form': form}
    return render(request, "accounts/register.html", context)

@unauthenticated_user
def loginPage(request):
    #if request.user.is_authenticated:
        #return redirect("home")
    #else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or password is incorrect")
    return render(request, "accounts/login.html")

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    context = {'orders': orders, 'orders_delivered':orders_delivered, 'orders_pending': orders_pending, 'total_orders': total_orders}
    return render(request, "accounts/user.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method=="POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, "accounts/account_settings.html", context)

@login_required(login_url="login")
#@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    #return HttpResponse("home")
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    context = {'orders':orders, 'customers': customers, 'orders_delivered':orders_delivered, 'orders_pending': orders_pending, 'total_orders': total_orders}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def products(request):
    #return HttpResponse("products")
    product = Product.objects.all()
    return render(request, 'accounts/products.html', {'product':product})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    #return HttpResponse("customer")
    customer = Customer.objects.get(id=pk)
    cust_orders = customer.order_set.all()
    total_cust_orders = cust_orders.count()
    myFilter = OrderFilter(request.GET, queryset=cust_orders)
    cust_orders = myFilter.qs
    context = {'customer': customer, 'orders':cust_orders, 'total_orders': total_cust_orders, 'myFilter':myFilter}
    return render(request, 'accounts/customers.html', context)

'''
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}
    return render(request, 'accounts/formstest.html', context)
'''

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)        
        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {'formset': formset}
    return render(request, 'accounts/formstest.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form': form}
    return render(request, 'accounts/formstest.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")
    context = {'item': order}
    return render(request, 'accounts/delete_order.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    customer = CustomerForm()
    if request.method == "POST":
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            customer.save()
            return redirect("/")
    context = {'customer': customer}
    return render(request, 'accounts/create_customer.html', context)
