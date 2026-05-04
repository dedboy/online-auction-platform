from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Bid
from django.shortcuts import render

def index(request):
    return render(request, 'index.html') # yoki shunchaki HttpResponse

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        amount = request.POST.get('bid_amount')
        # Garov narxi boshlang'ich narxdan balandligini tekshiramiz
        if float(amount) > float(product.start_price):
            Bid.objects.create(product=product, user=request.user, amount=amount)
            # Mahsulotning joriy narxini yangilaymiz
            product.start_price = amount
            product.save()
            return redirect('product_detail', product_id=product.id)

    return render(request, "auction/product_detail.html", {"product": product})