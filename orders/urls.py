from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_history, name='order-history'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('api/process-order/', views.process_order, name='process-order'),
    path('detail/<int:pk>/', views.order_detail, name='order-detail'),
]