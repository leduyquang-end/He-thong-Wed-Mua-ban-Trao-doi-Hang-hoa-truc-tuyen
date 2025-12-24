from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ('price', 'product_name')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'user', 'full_name', 'total_amount', 'status', 'created_at', 'is_paid')
    list_filter = ('status', 'created_at', 'is_paid')
    search_fields = ('order_code', 'full_name', 'phone')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)