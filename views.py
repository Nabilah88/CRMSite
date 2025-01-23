from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import*
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='login')
@admin_only
def home(request):   
    orders= Orders.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    total_order = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    
    
    context = {'orders':orders, 'customers':customers, 'total_customers': total_customers, 'total_order':total_order,
               'delivered': delivered, 'pending': pending}
    
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def UserPage(request):
    orders = request.user.customer.orders_set.all()
    total_order = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    
    print("ORDERS:", orders)
     
    context = {'orders':orders, 'total_order':total_order,
               'delivered': delivered, 'pending': pending}
    
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid():
            form.save()
            
    context ={'form': form}
    return render(request, 'accounts/account_settings.html', context)


def create_customer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form= CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
    context ={'form': form}
    return render(request, 'accounts/create_customer.html', context)
    

@unauthenticated_user
def register(request):
    
    form =CreateUserForm() 
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
                                                                    
      
    
    context={'form': form} 
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    
    if request.method == 'POST':
        username =request.POST.get('username')
        password =request.POST.get('password')
        
        user = authenticate(request, username= username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'USERNAME or PASSWORD is incorrect')
        
        
    context={} 
    return render(request, 'accounts/login.html', context)

def products(request):
    products = Products.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def organization(request): 
    posts = Posts.objects.all()
    return render(request, 'accounts/organization.html',{'posts': posts} )

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.orders_set.all()
    order_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset= orders)
    orders = myFilter.qs
    
    context = {'customers':customers, 'orders': orders, 'order_count':order_count, 'myFilter':myFilter}
    
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Orders,fields = ('product', 'status'), extra=5)
    customers = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset= Orders.objects.none(),instance=customers)
    
    if request.method == 'POST':
        formset = OrderForm(request.POST, instance = customer)
        if formset.is_valid():
             formset.save()
        return redirect('/')
        
    context = {'formset': formset }
    return render(request,'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Orders.objects.get(id=pk)
    formset = OrderForm(instance=order)
    if request.method == 'POST':
        formset = OrderForm(request.POST,instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context = {'formset': formset }
    
    return render(request,'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Orders.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
        
    context = {'item': order }
    return render(request,'accounts/delete_item.html', context)




# Create your views here.
