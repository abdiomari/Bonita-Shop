from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.db.models import Q
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django_user_agents.utils import get_user_agent
import random
from datetime import date
import logging

from .models import *
from .forms import  CustomUserCreationForm

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    products = list(Product.objects.all())
    category = list(Category.objects.all())
    week_of_year = date.today().isocalendar()[1]
    random.seed(week_of_year)

    featured_products = random.sample(products, 4)
    latest_products = Product.objects.order_by('-created_at')[:4]
    
    featured_category = random.choice(category)
    featured_category_products = [product for product in products if product.category == featured_category]
    
    if len(featured_category_products) < 3:
        featured_category_products = featured_category_products
    else:
        # Select 3 random products from the category
        featured_category_products = random.sample(featured_category_products, 3)
    
    return render(request, 'store/index.html', {
        'featured_products': featured_products, 
        'featured_category_products': featured_category_products,
        'latest_products': latest_products,
        'featured_category': featured_category
        })


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    user_agent = get_user_agent(request)
    
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by in categories.values_list('name', flat=True):
        products = products.filter(category__name=sort_by)  
    elif sort_by == 'name':
        products = products.order_by('-name')  
    elif sort_by == 'default':
        products = products.order_by('?')
    
    
    if user_agent.is_mobile:
        items_per_page = 6
    else:
        items_per_page = 8
        
    paginator = Paginator(products, items_per_page)
    
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    

    return render(request, 'store/products.html', {'products': products, 'categories': categories})

@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    return render(request, 'store/product_details.html', {'product': product, 'related_products': related_products})

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
    return render(request, 'store/account.html', {'form': form})

def CustomLoginView(request):
    if request.method == 'POST':
        username_or_email = request.POST['login']
        password = request.POST['password']

        User = get_user_model()
        try:
            # Check if a user exists with either the username or email
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            # If the user exists and the password is correct, log them in
            login(request, user)
            messages.success(request, "Welcome Back")
            return redirect('product_list')
        else:
            messages.error(request, "Please enter a correct username/email and password.")
            logger.warning(f"Failed login attempt for {username_or_email}")
    
    return render(request, 'store/account.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('account_login')

def account_setting(request):
    pass

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')