from django.db import models
from django.contrib.auth.models import User

# Model Sản phẩm
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    price = models.IntegerField(verbose_name="Giá")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Ảnh")
    description = models.TextField(verbose_name="Mô tả chi tiết", blank=True)

    def __str__(self):
        return self.name

# Model Giỏ hàng
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity