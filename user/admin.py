# coding=UTF-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import MyUserChangeForm, MyUserCreationForm
from .models import User as MyUser, Permission, Group


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nick', 'phone', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'nick', 'phone', 'email', 'is_staff')
    list_editable = ('nick', 'phone')
    filter_horizontal = ('groups', 'permissions',)
    raw_id_fields = ('groups', 'permissions',)
    search_fields = ('username', 'nick', 'phone', 'email')
    form = MyUserChangeForm
    add_form = MyUserCreationForm


class PermissionInline(admin.TabularInline):
    model = Group.permissions.through


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    inlines = [PermissionInline]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [PermissionInline]
    exclude = ('permissions',)
