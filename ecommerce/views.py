import json
from django.http import HttpResponseRedirect, JsonResponse
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

'''

AUTHENTICATION

'''

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

'''

PRODUCT MANAGEMENT

'''

@login_required
def product_single(request, product_id):
    product = Product.objects.get(pk=product_id)
    comments = Comment.objects.filter(product_id=product_id)
    rating = Comment.objects.filter(product_id=product_id).aggregate(Avg('rating'))
    rating2 = rating.get('rating__avg')

    chkcomment = Comment.objects.filter(user=request.user, product_id=product_id)

    context = {
        'categories': Category.objects.all(),
        'product':product,
        'comments': comments,
        'rating': rating2,
        'chkcomment': chkcomment,
        }

    return render(request, "ecommerce/product-single.html", context)

@login_required
def categories(request, category_id):
    products = Product.objects.filter(Category=category_id)

    context = {
        'categories': Category.objects.all(),
        'products': products,
    }
    return render(request, "ecommerce/category.html", context)
    

''' ADD COMMENT '''
@login_required
def comment(request, product_id):
    product = Product.objects.get(pk = product_id)
    msg = request.POST.get('msg')
    rating = int(float(request.POST.get('rating')))
    user = request.user
    com = Comment(user=user, product_id=product, rating=rating, msg=msg)
    com.save()
    return redirect('home')

'''

CART  - CHECKOUT - PAYMENT

'''

@login_required
def add_cart(request, product_id):
    product, created = Product.objects.get_or_create(Product, pk=product_id)
    order, created = Order.objects.get_or_create(customer=request.user)
    order.product.add(product_id)
    return HttpResponseRedirect(reverse('home'))

@login_required
def delete_cart(request, product_id):
    product, created = Product.objects.get_or_create(Product, pk=product_id)
    order, created = Order.objects.get_or_create(customer=request.user)
    order.product.remove(product_id)
    return redirect('cart')

@login_required
def cart(request):
    context = {
        'categories': Category.objects.all(),
        'user': request.user,
        'orders': Order.objects.all(),
    }
    return render(request, "ecommerce/cart.html", context)

@login_required
def checkout(request):

    orders = Order.objects.all()

    subtotal = []

    for order in orders:
        if order.customer == request.user:
            for data in order.product.all() :
                subtotal.append(data.price)

    total = int(sum(subtotal))

    vat = 0.21

    total_vat = total + (total*vat)

    print('AAAAAAAAAAAA', subtotal)
    print('THE TOTAL IS: ', total)
    print('THE TOTAL + VAT IS: ', total_vat)

    context = {
        'categories': Category.objects.all(),
        'total': total,
        'total_vat': total_vat,
    }
    return render(request, "ecommerce/checkout.html", context)