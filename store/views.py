from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CustomAuthenticationForm, CustomUserCreationForm


# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('product_list')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items )
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('product_list')  # Redirect to the product list after registration
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

# class CustomLoginView(View):
#     template_name = 'auth/login.html'
#     redirect_authenticated_user = True

#     def get(self, request, *args, **kwargs):
#         form = CustomAuthenticationForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = CustomAuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)  # Log the user in
#             return redirect('product_list')  # Redirect to the product list
#         else:
#             print("Login failed:", form.errors)  # Debugging output
#         return render(request, self.template_name, {'form': form})
from django.contrib.auth import authenticate, login

def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Please enter a correct username and password.")
    
    return render(request, 'auth/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('account_login')