from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('search/', views.search_view, name='search'),
    
    # --- NHÓM GIỎ HÀNG ---
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'), # Xóa
    path('update-cart/<int:pk>/<str:action>/', views.update_cart, name='update-cart'),   # Tăng/Giảm

    # --- NHÓM THANH TOÁN ---
    path('checkout/', views.checkout_view, name='checkout'),
]