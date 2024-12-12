from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import BookForm, OrderForm, SignupForm
from .models import Book, Cart, CartItem, Order

def signup(request):
    """Handle user registration with custom SignupForm."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already registered. Please try logging in.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered. Please try logging in.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Account created successfully. You can now log in.")
                return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'bookstore_app/signup.html', {'form': form})


# Authentication Views
@csrf_exempt
def user_login(request):
    """Handle user login with username and password."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                cart = CartManager.get_cart(request) or CartManager.create_cart(request)
                cart_items = request.session.pop('cart_items', [])

                for item in cart_items:
                    book = get_object_or_404(Book, id=item['book_id'])
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
                    if created:
                        cart_item.quantity = item['quantity']
                    else:
                        cart_item.quantity += item['quantity']
                    cart_item.total_price = cart_item.book.price * cart_item.quantity
                    cart_item.save()

                messages.success(request, 'Login successful!')
                return redirect('book_list')
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'bookstore_app/login.html')


# Book Management Views
@login_required
def book_list(request):
    """Display all books."""
    genre_filter = request.GET.get('genre', '')
    books = Book.objects.filter(genre__icontains=genre_filter)
    return render(request, 'bookstore_app/base.html', {
        'books': books,
        'genres': Book.objects.values_list('genre', flat=True).distinct(),
        'is_staff': request.user.is_staff
    })

@login_required
def add_book(request):
    """Add a new book to the store."""
    if not request.user.is_staff:
        return redirect('book_list')
        
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookstore_app/add_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    """Delete a book from the store."""
    if request.user.is_staff:
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        messages.success(request, f'"{book.title}" deleted successfully.')
    return redirect('book_list')

# Cart Manager Class
class CartManager:
    """Handle all cart-related operations."""
    
    @staticmethod
    def get_cart(request):
        """Retrieve or create cart for the logged-in user."""
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            return cart
        else:
            # Fallback to session-based cart for anonymous users
            cart_id = request.session.get('cart_id')
            if not cart_id:
                return None
        return Cart.objects.filter(id=cart_id).first()

    @staticmethod
    def create_cart(request):
        """Create a new cart for the logged-in user or session."""
        if request.user.is_authenticated:
            cart = Cart.objects.create(user=request.user)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        return cart

    @staticmethod
    def calculate_total(cart):
        """Calculate total price for cart items."""
        return sum(item.total_price for item in cart.cart_items.all())

# Order Manager Class
class OrderManager:
    """Handle all order-related operations."""
    
    @staticmethod
    def create_order(cart):
        """Create a new order from cart contents."""
        return Order.objects.create(
            cart=cart,
            total_price=cart.total_price
        )

    @staticmethod
    def clear_cart(request):
        """Remove all items from cart and delete it."""
        cart = CartManager.get_cart(request)
        if cart:
            cart.cart_items.all().delete()
            cart.delete()
            request.session.pop('cart_id', None)

# Cart Management Views
@login_required
def cart(request):
    """Display cart contents."""
    cart = CartManager.get_cart(request)
    total_price = CartManager.calculate_total(cart) if cart else 0
    return render(request, 'bookstore_app/cart.html', {
        'cart': cart,
        'total_price': total_price
    })

def get_cart_count(request):
    """Return current cart item count as JSON."""
    cart = CartManager.get_cart(request)
    count = sum(item.quantity for item in cart.cart_items.all()) if cart else 0
    return JsonResponse({'count': count})

@login_required
def update_quantity(request, book_id):
    """Update quantity of a book in the cart."""
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = CartManager.get_cart(request)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                
            cart_item.total_price = cart_item.quantity * cart_item.book.price
            cart_item.save()
            
            cart.total_price = CartManager.calculate_total(cart)
            cart.save()
            
            messages.success(request, 'Cart updated successfully!')
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            messages.error(request, 'Error updating cart.')
            
    return redirect('cart')

@login_required
def add_to_cart(request, book_id):
    """Add a book to the cart."""
    book = get_object_or_404(Book, id=book_id)
    cart = CartManager.get_cart(request) or CartManager.create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if created:
        cart_item.total_price = book.price
    else:
        cart_item.quantity += 1
        cart_item.total_price = book.price * cart_item.quantity
    
    cart_item.save()
    cart.total_price = CartManager.calculate_total(cart)
    cart.save()
    
    messages.success(request, f'"{book.title}" added to cart.')
    return redirect('book_list')

@login_required
def remove_from_cart(request, book_id):
    """Remove a book from the cart."""
    book = get_object_or_404(Book, id=book_id)
    cart = CartManager.get_cart(request)
    
    if not cart:
        messages.warning(request, 'Cart not found.')
        return redirect('cart')
    
    cart_item = CartItem.objects.filter(cart=cart, book=book).first()
    if not cart_item:
        messages.warning(request, f'"{book.title}" not in cart.')
        return redirect('cart')
        
    cart_item.delete()
    cart.total_price = CartManager.calculate_total(cart)
    cart.save()
    
    messages.success(request, f'"{book.title}" removed from cart.')
    return redirect('cart')

@csrf_exempt
def sync_cart(request):
    """Sync cart from localStorage to the server."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
        
    try:
        cart_data = json.loads(request.body).get('cart', [])
        cart = CartManager.get_cart(request) or CartManager.create_cart(request)

        for item in cart_data:
            book = Book.objects.get(id=item['book_id'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            if created:
                cart_item.quantity = item['quantity']
            else:
                cart_item.quantity += item['quantity']
            cart_item.total_price = book.price * cart_item.quantity
            cart_item.save()

        cart.total_price = CartManager.calculate_total(cart)
        cart.save()

        return JsonResponse({'success': True}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def get_cart_items(request):
    """API to fetch current cart items for the logged-in user."""
    cart = CartManager.get_cart(request)
    if not cart:
        return JsonResponse({'cart': []}, status=200)

    items = [{
        'book_id': item.book.id,
        'quantity': item.quantity,
        'price': item.total_price,
    } for item in cart.cart_items.all()]
    
    return JsonResponse({'cart': items}, status=200)

# Order Management Views
@login_required
def checkout(request):
    """Process checkout and ask for address."""
    cart = CartManager.get_cart(request)
    if not cart:
        messages.error(request, 'Cart not found.')
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                cart=cart,
                total_price=cart.total_price
            )
            OrderManager.clear_cart(request)
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'bookstore_app/checkout.html', {'form': form, 'cart': cart})

@login_required
def order_confirmation(request):
    """Display order confirmation page."""
    cart = CartManager.get_cart(request)
    if not cart:
        return redirect('book_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = OrderManager.create_order(cart)
            OrderManager.clear_cart(request)
            return render(request, 'bookstore_app/order_confirmation.html', {'order': order})
    else:
        form = OrderForm()
    
    return render(request, 'bookstore_app/order_confirmation.html', {
        'form': form,
        'cart': cart
    })

def order_success(request):
    """Display order success page."""
    return render(request, 'bookstore_app/order_success.html')

def logout_view(request):
    """Handle user logout."""
    cart = CartManager.get_cart(request)
    if cart and not request.user.is_authenticated:
        # Save cart items to session for anonymous users
        cart_items = [
            {'book_id': item.book.id, 'quantity': item.quantity}
            for item in cart.cart_items.all()
        ]
        request.session['cart_items'] = cart_items
    logout(request)
    request.session.pop('cart_id', None)  # Remove session-based cart
    messages.success(request, "Successfully logged out.")
    return redirect('login')