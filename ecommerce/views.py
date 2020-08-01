from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, "ecommerce/login.html")
    else:
        return render(request, "ecommerce/home.html")

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
            return redirect('login')
    context = {'form':form}
    return render(request, "ecommerce/register.html", context)
    