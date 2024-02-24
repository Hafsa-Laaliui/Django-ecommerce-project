from django.shortcuts import render , redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Product, Order , Category , Cart, CartItem
from django.urls import reverse_lazy
from django.db.models import Q 
from django.http import JsonResponse
import json
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm, AddToCartForm,ShippingForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, AddToCartForm
from django.contrib import messages

class ProductsListView(ListView):
    template_name = 'list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id)

class ProductDetailView(DetailView):  # Renamed from BooksDetailView
    model = Product
    template_name = 'detail.html'

class SearchResultsListView(ListView):
    model = Product
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query) # Adjusted search fields
        )

class ProductCheckoutView(LoginRequiredMixin, DetailView):  # Renamed from BookCheckoutView
    model = Product
    template_name = 'checkout.html'
    login_url = 'login'

def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Product.objects.get(id=body['productId'])
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment completed!', safe=False)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Assuming you have a user field in your Order model
            order.save()
            return redirect('order_history')
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

# Example of updating order status (you can modify it based on your requirements)
@login_required
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user.is_staff:  # Only staff can update order status (customize as needed)
        if request.method == 'POST':
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()
            return redirect('order_detail', order_id=order.id)
    return render(request, 'update_order_status.html', {'order': order})

# Example of generating order invoice (customize as needed)
@login_required
def generate_order_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_invoice.html', {'order': order})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to the desired page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')



def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            
            # Get or create the cart for the current user
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Add the product to the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            
            # Optionally, you can display a success message
            messages.success(request, f'{product.title} has been added to your cart.')
            
            return redirect('cart')  # Redirect to the cart page after adding the product
    else:
        form = AddToCartForm()
    return render(request, 'add_to_cart.html', {'form': form})


def view_cart(request):
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Fetch all cart items associated with the current cart
    cart_items = cart.cartitem_set.all()
    
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


def update_cart(request):
    if request.method == 'POST':
        for cart_item_id, quantity in request.POST.items():
            if cart_item_id.isdigit():
                cart_item = get_object_or_404(CartItem, id=cart_item_id)
                cart_item.quantity = int(quantity)
                cart_item.save()
    return redirect('cart')

def cart_count(request):
    # Retrieve the cart count from the database or session
    cart_count = Cart.objects.filter(user=request.user).count()  # Example query
    return JsonResponse({'cart_count': cart_count})


def checkout_view(request):
    return render(request, 'checkout.html')
