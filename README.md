# 📚 BookStore_Django

## Welcome to the Bookstore E-commerce Application! 🎉

An intuitive and feature-rich e-commerce platform designed for book lovers. Browse your favorite books, add them to a cart, and complete your purchases seamlessly. Staff members enjoy extended privileges to manage inventory effectively. Dive into the world of books with a delightful shopping experience!

---

## 🌟 Features

### 👤 User Management
- **Signup**: Effortlessly create an account with a username, email, and password. Duplicate username or email? We’ve got you covered!
- **Login**: Log in to your account and sync cart items across devices.
- **Logout**: Sign out while keeping your cart items safe for later.

### 📚 Book Management
- **Book List**: Explore the entire catalog with genre-based filtering.
- **Add Book**: Staff can enrich the catalog by adding new books with all details.
- **Delete Book**: Staff can declutter the catalog by removing outdated books.

### 🛒 Cart Management
- **View Cart**: Keep track of selected books and their total price.
- **Add to Cart**: Add your favorite books to the shopping cart.
- **Update Quantity**: Adjust the number of copies directly in the cart.
- **Remove from Cart**: Declutter your cart by removing unwanted items.
- **Cart Sync**: Access your updated cart seamlessly across devices.
- **Cart Count**: Always stay updated with the number of items in your cart.

### 📦 Order Management
- **Checkout**: A simple and secure process to finalize your purchase.
- **Order Confirmation**: Double-check order details before confirming.
- **Order Success**: Celebrate with a confirmation message for your successful order.

### 🛠️ Helper Classes
- **CartManager**: Handles all cart operations, ensuring smooth shopping experiences.
- **OrderManager**: Streamlines order creation and clears cart post-purchase.

---

## 🚀 Setup

### 1️⃣ Clone the Repository:
```bash
git clone https://github.com/yourusername/bookstore-app.git
cd bookstore-app
```

### 2️⃣ Configure Media Files:
Update the MEDIA_ROOT in settings.py to set the path for uploaded media files:

```
MEDIA_ROOT = '/yourpath'
```
### 3️⃣ Install Dependencies:
Ensure all necessary packages are installed:

```bash
pip install -r requirements.txt
```
### 4️⃣ Run the Application:
Start the development server:
```bash
python manage.py runserver
```
### 5️⃣ Access the Application:
Open your browser and navigate to: http://127.0.0.1:8000/

## 👥 Usage

### For Users:
Sign up and log in to discover a world of books.
Add your favorites to the cart, adjust quantities, and proceed to checkout.
Enjoy seamless cart syncing across all your devices!

### For Staff Members:
Manage inventory effortlessly by adding or removing books.
Stay on top of operations by reviewing and fulfilling orders.

## 🤝 Contributing
We welcome contributions! Feel free to fork the repository, make your improvements, and submit a pull request.

## 🌟 Acknowledgments
Special thanks to Django for its robust framework and the entire community for inspiration. Happy coding! 😊
