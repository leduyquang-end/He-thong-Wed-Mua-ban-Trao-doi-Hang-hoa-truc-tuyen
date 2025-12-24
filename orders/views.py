from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from store.models import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
import json

@login_required(login_url='login')
def checkout_view(request):
    item_ids = request.GET.get('items', '')
    
    if not item_ids:
        return redirect('cart')

    try:
        id_list = [int(x) for x in item_ids.split(',')]
    except ValueError:
        return redirect('cart')

    cart_items = Cart.objects.filter(user=request.user, id__in=id_list)

    if not cart_items:
        return redirect('cart')

    total_pre_sale = 0
    total_final = 0

    for item in cart_items:
        total_pre_sale += item.product.price * item.quantity
        total_final += item.product.current_price * item.quantity

    discount_amount = total_pre_sale - total_final

    form = OrderCreateForm()
    user_profile = getattr(request.user, 'profile', None)

    context = {
        'cart_items': cart_items,
        'total_pre_sale': total_pre_sale,
        'total_final': total_final,
        'discount_amount': discount_amount,
        'form': form,
        'user_profile': user_profile,
        'selected_item_ids': item_ids
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def process_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            order = Order.objects.create(
                user=request.user,
                full_name=data.get('full_name'),
                phone=data.get('phone'),
                address=data.get('address'),
                note=data.get('note'),
                total_amount=data.get('total_amount'),
                payment_method=data.get('payment_method'),
                is_paid=(data.get('payment_method') == 'QR')
            )

            item_ids_str = data.get('item_ids', '')
            if item_ids_str:
                id_list = [int(x) for x in item_ids_str.split(',')]
                cart_items = Cart.objects.filter(user=request.user, id__in=id_list)
            else:
                cart_items = []

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.current_price,
                    quantity=item.quantity
                )

            if cart_items:
                cart_items.delete()

            return JsonResponse({'success': True, 'order_code': order.order_code})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': "Invalid Request"})

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'orders/order_history.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
        'item_count': items.count() 
    }
    return render(request, 'orders/order_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Order

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items = order.items.all()
    
    temp_total = 0
    for item in items:
        if item.product: 
            temp_total += item.product.price * item.quantity
        else:
            temp_total += item.price * item.quantity
    savings = temp_total - order.total_amount
    if savings < 0: savings = 0 

    context = {
        'order': order,
        'items': items,
        'item_count': items.count(),
        'temp_total': temp_total, 
        'savings': savings, 
    }
    return render(request, 'orders/order_detail.html', context)