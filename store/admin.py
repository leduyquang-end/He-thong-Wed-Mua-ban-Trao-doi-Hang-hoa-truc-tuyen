from django.contrib import admin
from .models import Product, Review, Contact
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'name', 'price', 'current_price', 'discount_percent', 'is_on_sale')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'product_code')
    readonly_fields = ('product_code',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'message', 'subject')
    
    list_editable = ('status',)
    
    readonly_fields = ('user', 'full_name', 'email', 'phone', 'subject', 'message', 'created_at')
    
    fieldsets = (
        ('Thông tin khách gửi', {
            'fields': ('full_name', 'email', 'phone', 'user', 'created_at')
        }),
        ('Nội dung', {
            'fields': ('subject', 'message')
        }),
        ('Xử lý (Internal)', {
            'fields': ('status', 'admin_note'),
            'description': 'Admin trả lời qua Email riêng, sau đó cập nhật trạng thái ở đây.'
        }),
    )

admin.site.register(Contact, ContactAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)