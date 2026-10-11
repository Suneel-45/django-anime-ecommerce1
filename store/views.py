from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, OrderItem

def _cart(request):
    return request.session.setdefault("cart", {})

def _cart_summary(request):
    cart = request.session.get("cart", {})
    items, total, count = [], Decimal("0.00"), 0
    ids = [int(pid) for pid in cart.keys() if str(pid).isdigit()]
    products = {p.id: p for p in Product.objects.filter(id__in=ids, is_active=True)}
    for pid, raw_qty in cart.items():
        if not str(pid).isdigit() or int(pid) not in products:
            continue
        product = products[int(pid)]
        qty = max(1, min(int(raw_qty), product.stock)) if product.stock else 0
        if qty == 0:
            continue
        line_total = product.price * qty
        items.append({"product": product, "quantity": qty, "line_total": line_total})
        total += line_total
        count += qty
    return items, total, count

def home(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query))
    return render(request, "store/home.html", {"products": products, "query": query})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})

def cart_add(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", product_id=product.id)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = min(int(cart.get(key, 0)) + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")

def cart_detail(request):
    items, total, count = _cart_summary(request)
    return render(request, "store/cart.html", {"items": items, "total": total, "cart_count": count})

def cart_update(request, product_id):
    if request.method != "POST":
        return redirect("cart")
    cart = request.session.get("cart", {})
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    if qty <= 0:
        cart.pop(str(product_id), None)
    elif product.stock:
        cart[str(product_id)] = min(qty, product.stock)
    else:
        cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")

def cart_remove(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
        messages.info(request, "Item removed from your cart.")
    return redirect("cart")

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("home")
    return render(request, "store/register.html", {"form": form})

@login_required
def checkout(request):
    items, total, count = _cart_summary(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    if request.method == "POST":
        fields = ["full_name", "email", "address", "city", "postal_code"]
        data = {field: request.POST.get(field, "").strip() for field in fields}
        if not all(data.values()):
            messages.error(request, "Please complete every checkout field.")
            return render(request, "store/checkout.html", {"items": items, "total": total, "data": data})
        try:
            with transaction.atomic():
                product_ids = [item["product"].id for item in items]
                locked = {p.id: p for p in Product.objects.select_for_update().filter(id__in=product_ids, is_active=True)}
                for item in items:
                    p = locked.get(item["product"].id)
                    if p is None or p.stock < item["quantity"]:
                        raise ValueError(f"Not enough stock for {item['product'].name}. Please update your cart.")
                order = Order.objects.create(user=request.user, total=total, **data)
                for item in items:
                    product = locked[item["product"].id]
                    qty = item["quantity"]
                    OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=product.price, quantity=qty)
                    product.stock -= qty
                    product.save(update_fields=["stock"])
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect("cart")
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.id} placed successfully. Payment is not collected in this demo.")
        return redirect("orders")
    return render(request, "store/checkout.html", {"items": items, "total": total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "store/orders.html", {"orders": orders})
