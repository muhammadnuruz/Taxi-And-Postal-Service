from django.contrib import admin
from django.contrib.auth.hashers import make_password, is_password_usable
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
    list_display_links = ('id', 'full_name')
    list_editable = ('is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('full_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('full_name', 'password')}),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('full_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        if obj.password and not obj.password.startswith('pbkdf2') and is_password_usable(obj.password):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
