# Cartify — Django E-commerce Store

A beginner-friendly e-commerce starter built with **HTML, CSS, JavaScript, Django, and SQLite**.

## Features
- Product listing page with search
- Product details pages
- Session-based shopping cart (add, update quantity, remove)
- User registration, login, and logout
- Checkout and order creation
- Order history for logged-in users
- Django admin to manage products and orders
- Demo products loaded by a seed command
- Responsive layout

> This is a learning/demo project. It does not collect payment details or integrate a payment gateway. Before production, add payment processing, security review, tests, email/order notifications, inventory locking, and deployment configuration.

## Requirements
- Python 3.10+
- pip

## Run locally

### 1. Extract and open the project
```bash
cd django_ecommerce_store
```

### 2. Create a virtual environment
Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Create database tables and demo products
```bash
python manage.py migrate
python manage.py seed_products
```

### 5. Create an admin account (optional)
```bash
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Main routes
- `/` — product listings and search
- `/products/<id>/` — product details
- `/cart/` — shopping cart
- `/checkout/` — place an order (login required)
- `/accounts/register/` — create an account
- `/accounts/login/` — login
- `/orders/` — your order history (login required)
- `/admin/` — product/order management

## Upload to GitHub
1. Create a new empty repository on GitHub.
2. Extract this ZIP file.
3. Open a terminal in the extracted folder.
4. Run:
```bash
git init
git add .
git commit -m "Build Django e-commerce store"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Replace the remote URL with your repository URL. Do not commit secrets, `.env` files, virtual environments, or a production database.

## Notes
- SQLite is configured for local development.
- Product images use remote Unsplash URLs as demo placeholders; replace them with your own licensed images if desired.
- The default Django development secret key and `DEBUG=True` are for local development only. Set environment-based secrets and production settings before deployment.
