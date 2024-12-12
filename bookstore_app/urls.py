from django.urls import path
from . import views

urlpatterns = [
    # User 
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Book 
    path('book_list/', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
    
    # Cart
    path('cart/', views.cart, name='cart'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('get_cart_items/', views.get_cart_items, name='get_cart_items'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:book_id>/', views.update_quantity, name='update_quantity'),
    path('sync_cart/', views.sync_cart, name='sync_cart'),
    
    # Order 
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order_confirmation, name='order_confirmation'),
    path('order_success/', views.order_success, name='order_success'),
]
