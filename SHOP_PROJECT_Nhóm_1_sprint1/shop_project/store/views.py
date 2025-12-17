from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from django.contrib import messages

# Trang chủ
def index(request):
    products = Product.objects.all()
    return render(request, "store/index.html", {'products': products})

# Xem chi tiết sản phẩm
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {'product': product})

# Thêm vào giỏ
@login_required(login_url='login') 
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# VIEW GIỎ HÀNG 
@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    # Tính tổng tiền: sum(giá * số lượng)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, "store/cart.html", context)

# XÓA SẢN PHẨM KHỎI GIỎ
@login_required(login_url='login')
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
    return redirect('cart')

# TĂNG/GIẢM SỐ LƯỢNG
@login_required(login_url='login')
def update_cart(request, pk, action):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1

    if cart_item.quantity < 1:
        cart_item.delete()
    else:
        cart_item.save()
        
    return redirect('cart')

# VIEW THANH TOÁN
@login_required(login_url='login')
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.warning(request, "Giỏ hàng trống, vui lòng mua hàng trước!")
        return redirect('home')

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    user_profile = getattr(request.user, 'profile', None)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'user_profile': user_profile
    }
    return render(request, "store/checkout.html", context)

# Tìm kiếm
def search_view(request):
    query = request.GET.get('q', '')
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.none()
        
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'store/search_results.html', context)