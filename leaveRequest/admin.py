from django.contrib import admin

from .models import User, Leave

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user_type')
    search_fields = ('name', 'email')

admin.site.register(User, UserAdmin)

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'leave_from', 'leave_to', 'leave_reason', 'leave_status')
    search_fields = ('user', 'leave_type', 'leave_from', 'leave_to', 'leave_reason', 'leave_status')

admin.site.register(Leave, LeaveAdmin)