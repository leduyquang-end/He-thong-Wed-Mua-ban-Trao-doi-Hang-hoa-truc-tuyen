from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import random
import string

def generate_product_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class Product(models.Model):
    # 1. Mã SP
    product_code = models.CharField(
        max_length=10, 
        unique=True, 
        default=generate_product_code, 
        editable=False,
        verbose_name="Mã sản phẩm"
    )

    # 2. Tên SP
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")

    # 3. Thông tin sản phẩm
    category = models.CharField(max_length=100, verbose_name="Loại sản phẩm", help_text="Ví dụ: Điện tử, Gia dụng, Thời trang...")
    brand = models.CharField(max_length=100, verbose_name="Hãng sản xuất", blank=True)
    product_series = models.CharField(max_length=100, verbose_name="Dòng sản phẩm", blank=True)
    release_year = models.IntegerField(verbose_name="Năm ra mắt", null=True, blank=True)
    dimensions = models.CharField(max_length=100, verbose_name="Kích thước (Dài x Rộng x Cao)", blank=True, help_text="Ví dụ: 20x30x50 cm")

    # 4. Mô tả & Ảnh
    description = models.TextField(verbose_name="Mô tả chi tiết", blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Ảnh minh họa")

    # 5. Giá thành & Giảm giá
    price = models.IntegerField(verbose_name="Giá gốc (VNĐ)")
    discount_percent = models.IntegerField(default=0, verbose_name="Phần trăm giảm (%)", help_text="Nhập 0 nếu không giảm")
    discount_start_date = models.DateTimeField(null=True, blank=True, verbose_name="Ngày bắt đầu giảm")
    discount_end_date = models.DateTimeField(null=True, blank=True, verbose_name="Ngày kết thúc giảm")

    # 6. Đánh giá sản phẩm
    average_rating = models.FloatField(default=0.0, verbose_name="Điểm đánh giá TB")
    review_count = models.IntegerField(default=0, verbose_name="Số lượt đánh giá")

    def __str__(self):
        return f"[{self.product_code}] {self.name}"

    @property
    def current_price(self):
        now = timezone.now()
        if (self.discount_percent > 0 and 
            self.discount_start_date and 
            self.discount_end_date and 
            self.discount_start_date <= now <= self.discount_end_date):
            
            discount_amount = self.price * (self.discount_percent / 100)
            return int(self.price - discount_amount)
        return self.price

    @property
    def is_on_sale(self):
        return self.current_price < self.price

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product.current_price * self.quantity
    
# Đánh giá người dùng (ID7)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Sản phẩm")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người đánh giá")
    RATING_CHOICES = (
        (1, '1 Sao - Tệ'),
        (2, '2 Sao - Kém'),
        (3, '3 Sao - Bình thường'),
        (4, '4 Sao - Tốt'),
        (5, '5 Sao - Tuyệt vời'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Điểm số")
    
    comment = models.TextField(max_length=500, blank=True, verbose_name="Nội dung đánh giá")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày sửa")

    class Meta:

#        unique_together = ('product', 'user')
        ordering = ['-created_at'] 

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

# Điểm đánh giá trung bình
@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    aggregate_data = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'), count=models.Count('id'))
    
    product.average_rating = aggregate_data['avg_rating'] or 0.0
    product.review_count = aggregate_data['count'] or 0
    product.save()

#CSKH
class Contact(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'Mới - Chưa đọc'),
        ('READ', 'Đã xem'),
        ('REPLIED', 'Đã gửi Email trả lời'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tài khoản (nếu có)")
    full_name = models.CharField(max_length=100, verbose_name="Họ tên người gửi")
    email = models.EmailField(verbose_name="Email nhận phản hồi")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="SĐT (Tùy chọn)")

    subject = models.CharField(max_length=200, verbose_name="Tiêu đề")
    message = models.TextField(verbose_name="Nội dung liên hệ")
    
#    attachment = models.FileField(upload_to='contact_files/', null=True, blank=True, verbose_name="Tệp đính kèm")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Trạng thái")
    admin_note = models.TextField(blank=True, null=True, verbose_name="Ghi chú nội bộ (Admin)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian gửi")

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

    class Meta:
        verbose_name = "Liên hệ / Góp ý"
        verbose_name_plural = "Danh sách Liên hệ"
        ordering = ['-created_at']