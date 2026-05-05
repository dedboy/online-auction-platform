from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Bid, Category
from .forms import SignUpForm, ProductForm
from django.contrib.auth import login
from django.utils import timezone
from decimal import Decimal, InvalidOperation

# Barcha mahsulotlar va Qidiruv
def index(request):
    query = request.GET.get('q')
    cat_id = request.GET.get('category')
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(title__icontains=query)
    if cat_id:
        products = products.filter(category_id=cat_id)
    categories = Category.objects.all()
    return render(request, 'auction/index.html', {'products': products, 'categories': categories})

# Ro'yxatdan o'tish
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'auction/signup.html', {'form': form})

# Mahsulot qo'shish (Sotish)
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.is_active = True
            product.save()
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'auction/add_product.html', {'form': form})

# Mahsulot tafsilotlari va Stavka qo'yish
@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    bids = product.bids.all().order_by('-timestamp')
    if request.method == 'POST':
        if product.end_time < timezone.now():
            return render(request, "auction/product_detail.html", {"product": product, "bids": bids, "error": "Auksion tugagan!"})
        amount_raw = request.POST.get('bid_amount')
        try:
            amount = Decimal(amount_raw.replace(',', '.'))
            if request.user.balance < amount:
                return render(request, "auction/product_detail.html", {"product": product, "bids": bids, "error": "Balans yetarli emas!"})
            current_max = product.current_price if product.current_price else product.start_price
            if amount > current_max:
                Bid.objects.create(product=product, user=request.user, amount=amount)
                product.current_price = amount
                product.save()
                return redirect('product_detail', product_id=product.id)
        except (InvalidOperation, ValueError):
            pass
    return render(request, "auction/product_detail.html", {"product": product, "bids": bids})

# Mening stavkalarim (User Dashboard)
@login_required(login_url='login')
def my_bids(request):
    products_ids = Bid.objects.filter(user=request.user).values_list('product_id', flat=True).distinct()
    user_products = Product.objects.filter(id__in=products_ids)
    return render(request, 'auction/my_bids.html', {'products': user_products})