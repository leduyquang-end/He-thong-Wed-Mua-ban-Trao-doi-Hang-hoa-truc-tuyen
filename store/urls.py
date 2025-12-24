from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('search/', views.search_view, name='search'),
    path('product/<int:pk>/review/', views.
         review, name='review'),
    
    # --- NHÓM GIỎ HÀNG ---
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'), 
    path('update-cart/<int:pk>/<str:action>/', views.update_cart, name='update-cart'), 
    # --- CSKH ---
    path('customer-support/', views.customer_support, name='customer_support'),
]