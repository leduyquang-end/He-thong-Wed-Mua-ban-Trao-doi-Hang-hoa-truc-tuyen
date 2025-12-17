from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    gender = models.CharField(
        max_length=10, 
        choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], 
        blank=True,
        verbose_name="Giới tính"
    )
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True,
        verbose_name="Ảnh đại diện"
    )

    def __str__(self):
        return f"Hồ sơ của {self.user.username}"