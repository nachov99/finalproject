from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.db.models import Avg

from .forms import CreateUserForm, ProductForm
from .models import Category, Product, Order, Comment

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, "ecommerce/login.html")
    else:
        context = {
            'categories': Category.objects.all(),
            'products': Product.objects.all(),
            'user': request.user,
        }
        return render(request, "ecommerce/index.html", context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect!')
    return render(request, "ecommerce/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out!')
    return redirect('login_view')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login_view')
    context = {'form':form}
    return render(request, "ecommerce/register.html", context)

@login_required
def add_cart(request, product_id):
    product, created = Product.objects.get_or_create(Product, pk=product_id)
    order, created = Order.objects.get_or_create(customer=request.user)
    order.product.add(product_id)
    return HttpResponseRedirect(reverse('home'))


def cart(request):
    order = Order.objects.filter(customer=request.user)
    context = {
        'order': order,
    }
    return render(request, "ecommerce/cart.html", context)

@login_required
def category_products(request, category_id):
    product_list = Product.objects.filter(Category = category_id)
    Categories = Category.objects.all()
    context = {
        'products': product_list,
        'categories': Categories
    }
    return render(request, "ecommerce/category_products.html", context)

@login_required
def order_list(request):
    Orders = Order.objects.all()

    context = {
        'orders': Orders,
    }
    return render(request, "ecommerce/orders.html", context)

@login_required
def add_product(request):

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}

    return render(request, "ecommerce/add_product.html", context)

@login_required
def product_single(request, product_id):
    product = Product.objects.get(pk=product_id)
    comments = Comment.objects.all()
    rating = Comment.objects.filter(product_id=product_id).aggregate(Avg('rating'))
    rating2 = rating.get('rating__avg')
    context = {
        'product':product,
        'comments': comments,
        'rating': rating2,
        }

    return render(request, "ecommerce/product-single.html", context)

''' ADD COMMENT '''
@login_required
def comment(request, product_id):
    product = Product.objects.get(pk = product_id)
    msg = request.POST.get('msg')
    rating = int(request.POST.get('rating'))
    user = request.user
    com = Comment(user=user, product_id=product, rating=rating, msg=msg)
    com.save()
    return redirect('home')


