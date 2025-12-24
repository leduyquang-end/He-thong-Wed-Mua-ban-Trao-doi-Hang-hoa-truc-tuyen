from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_code', 'full_name', 'phone', 'gender')
    search_fields = ('user__username', 'user_code', 'phone')
    readonly_fields = ('user_code',)

admin.site.register(Profile, ProfileAdmin)