from django.db import models
from django.contrib.auth.models import User
from store.models import Product
import random
import string

def generate_order_code():
    return 'DH' + ''.join(random.choices(string.digits, k=8))

# --- MODEL 1: THÔNG TIN CHUNG CỦA ĐƠN HÀNG (HEADER) ---
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Chờ xác nhận'),
        ('Confirmed', 'Đã xác nhận'),
        ('Shipping', 'Đang giao hàng'),
        ('Delivered', 'Giao thành công'),
        ('Cancelled', 'Đã hủy'),
    ]

    order_code = models.CharField(max_length=20, default=generate_order_code, unique=True, editable=False, verbose_name="Mã đơn hàng")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Khách hàng")

    full_name = models.CharField(max_length=100, verbose_name="Tên người nhận")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.TextField(verbose_name="Địa chỉ giao hàng")
    
    total_amount = models.IntegerField(verbose_name="Tổng tiền đơn hàng")
    payment_method = models.CharField(max_length=50, default="COD", verbose_name="Phương thức thanh toán")
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán chưa")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt hàng")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày giao thành công") 

    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú đơn hàng")

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f"Đơn {self.order_code} - {self.user.username}"


# --- MODEL 2: CHI TIẾT TỪNG SẢN PHẨM TRONG ĐƠN (ITEMS) ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    
    product_name = models.CharField(max_length=200, verbose_name="Tên SP lúc mua") 
    price = models.IntegerField(verbose_name="Giá lúc mua")
    
    quantity = models.IntegerField(default=1, verbose_name="Số lượng")

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def get_cost(self):
        return self.price * self.quantity