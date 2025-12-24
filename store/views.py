from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, Contact, Review
from .forms import ContactForm, ReviewForm
from django.core.paginator import Paginator

# Trang chủ
def index(request):
    products = Product.objects.all().order_by('-id')
    return render(request, "store/index.html", {'products': products})

# Xem chi tiết sản phẩm
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    reviews_list = Review.objects.filter(product=product).order_by('-created_at')
    paginator = Paginator(reviews_list, 10) 
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    
    context = {
        'product': product,
        'reviews': reviews 
    }
    
    return render(request, "store/product_detail.html", context)

# Thêm vào giỏ
@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Đã thêm {product.name} vào giỏ!")
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)
    return redirect('home')

# VIEW GIỎ HÀNG 
@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    total_price = sum(item.product.current_price * item.quantity for item in cart_items)
    
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

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        query_lower = query.lower().strip()

        all_products = Product.objects.all().order_by('-id')
        
        for product in all_products:
            if (query_lower in product.name.lower() or 
                query_lower in (product.brand or '').lower() or 
                query_lower in product.category.lower() or 
                query_lower in product.product_code.lower()):
                
                results.append(product)
    else:
        results = []
        
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'store/search_results.html', context)

# --- CSKH (ID9) ---
def customer_support(request):
    initial_data = {}
    if request.user.is_authenticated:
        full_name = f"{request.user.last_name} {request.user.first_name}".strip()
        if not full_name:
            full_name = request.user.username
        initial_data = {
            'full_name': full_name,
            'email': request.user.email
        }

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            messages.success(request, "Cảm ơn bạn! Yêu cầu hỗ trợ đã được gửi.")
            return redirect('home')
    else:
        form = ContactForm(initial=initial_data)

    return render(request, 'store/customer_support.html', {'form': form})

@login_required(login_url='login')
def review(request, pk):
    from orders.models import OrderItem
    product = get_object_or_404(Product, pk=pk)
    
    has_received = OrderItem.objects.filter(
        order__user=request.user, 
        product=product,
        order__status='Delivered'
    ).exists()

    if not has_received:
        messages.warning(request, "Bạn chỉ có thể đánh giá sản phẩm sau khi đơn hàng được giao thành công!")
        return redirect('product-detail', pk=product.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.product = product
            new_review.save()
            
            messages.success(request, "Cảm ơn bạn đã gửi thêm đánh giá!")
            return redirect('product-detail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'store/review.html', {'product': product, 'form': form})