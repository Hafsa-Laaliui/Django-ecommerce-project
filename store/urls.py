from django.urls import path
from .views import (
    ProductsListView,  # Updated import statement
    ProductDetailView,  # Updated import statement
    ProductCheckoutView,  # Updated import statement
    paymentComplete,
    SearchResultsListView,
    about,
    contact,
    home,
    place_order,  
    order_history,  
    update_order_status,
    logout_view,
    register,
    login_view,
    add_to_cart,
    remove_from_cart,
    update_cart,
    view_cart,
    cart_count,
    checkout_view,
)

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'), 
    path('<int:pk>/checkout/', ProductCheckoutView.as_view(), name='checkout'),  
    path('complete/', paymentComplete, name='complete'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('', home, name='home'),
    path('category/', home, name='base'),
    path('categories/<int:category_id>/', ProductsListView.as_view(), name='list'),
    path('place_order/', place_order, name='place_order'),
    path('order_history/', order_history, name='order_history'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/', update_cart, name='update_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/count/', cart_count, name='cart_count'),
    path('checkout/', checkout_view, name='checkout'),


]
