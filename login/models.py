from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Hàm tạo mã User: U + 9 số ngẫu nhiên
def generate_user_code():
    while True:
        number = random.randint(100000000, 999999999)
        code = f"U{number}"
        if not Profile.objects.filter(user_code=code).exists():
            return code

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
        ('Khác', '----'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 1. Mã User
    user_code = models.CharField(max_length=10, default=generate_user_code, unique=True, editable=False, verbose_name="Mã User")
    
    # 2. Các thông tin cá nhân
    display_name = models.CharField(max_length=50, blank=True, verbose_name="Tên hiển thị (Nickname)")
    full_name = models.CharField(max_length=100, blank=True, verbose_name="Tên thật (Để nhận hàng)")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, verbose_name="Địa chỉ nhà mặc định")
    
    # 3. Thông tin bổ sung
    birth_date = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Khác', verbose_name="Giới tính")
    
    profile_picture = models.ImageField(default='default_avatar.png', upload_to='profile_pics', verbose_name="Ảnh đại diện")

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()