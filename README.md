# BookStore_Django

# Bookstore E-commerce Application

This is a e-commerce application designed for a bookstore where users can browse books, add them to a cart, and complete purchases. Staff members have additional privileges to manage the inventory. The application follows a typical shopping flow with user management, book management, cart management, and order management features.

## Features

### User Management
- **Signup**: Allows new users to create an account by providing a username, email, and password. It checks if the username or email is already taken before creating the account.
- **Login**: Allows users to sign in using their username and password. If users had items in their cart before logging in, those items are transferred to their account.
- **Logout**: Allows users to sign out of their account while saving their cart items for when they return.

### Book Management
- **Book List**: Displays all available books with an option to filter them by genre.
- **Add Book**: Staff members can add new books to the store, including details like title, price, and genre.
- **Delete Book**: Staff members can remove books from the store.

### Cart Management
- **View Cart**: Shows the books in the shopping cart and their total price.
- **Add to Cart**: Allows users to add books to their shopping cart.
- **Update Quantity**: Allows users to increase or decrease the number of copies of a book in their cart.
- **Remove from Cart**: Allows users to remove books from their cart.
- **Cart Sync**: Syncs the cart across different devices, keeping it updated on the server.
- **Cart Count**: Displays the number of items in the cart.

### Order Management
- **Checkout**: Starts the process of purchasing books by collecting delivery information.
- **Order Confirmation**: Shows the details of the order before it is confirmed.
- **Order Success**: Displays a confirmation page after an order is successfully placed.

### Helper Classes
- **CartManager**: Handles all shopping cart operations such as creating new carts, finding existing carts, and calculating total prices.
- **OrderManager**: Manages order-related tasks like creating new orders from cart contents and clearing the cart after an order is placed.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/bookstore-app.git
   cd bookstore-app

2. **Update Media Path:**
   Update the MEDIA_ROOT in settings.py to specify the location for media files:
   MEDIA_ROOT = '/yourpath'

3.**Run the Application:** 
  Start the application server:
  python manage.py runserver

4.**Access the App:**
  Open your browser and go to http://127.0.0.1:8000/ to view the bookstore application.

## Usage

For Users:
  - Sign up and log in to start browsing books.
  - Add books to your cart, update quantities, and proceed to checkout to place an order.
  - Your cart items are saved and can be accessed on different devices after login.

For Staff Members:
  - Staff members can add and delete books from the store.
  - Staff members can manage the entire inventory and review orders.


