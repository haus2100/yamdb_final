from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api_yamdb.settings import EMPTY_VALUE
from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdminConfig(UserAdmin):
    default_site = 'api_yamdb.users.admin.AdminAreaSite'
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'is_active',
        'date_joined'
    )
    search_fields = ('username', 'email')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        ('Key fields', {
            'fields': ('username', 'email', 'password', 'role')
        }),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'bio'
            ), 'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff',),
        }),
        ('Date joined', {
            'fields': ('date_joined',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('extrapretty',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user.is_staff and not obj.is_staff
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_staff and not obj.is_staff
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def save_model(self, request, obj, form, change):
        if isinstance(obj, User):
            super().save_model(request, obj, form, change)
            user_role = obj.role
            if user_role == User.ADMIN:
                obj.is_staff = True
            # на случай изменения объекта
            else:
                obj.is_staff = False
            obj.save()
        else:
            super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdminConfig(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'text',
        'pub_date'
    )
    empty_value_display = EMPTY_VALUE


@admin.register(Review)
class ReviewAdminConfig(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'score',
        'author',
        'pub_date'
    )
    empty_value_display = EMPTY_VALUE


@admin.register(Category)
class CategoryAdminConfig(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


@admin.register(Genre)
class GenreAdminConfig(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


@admin.register(Title)
class TitleAdminConfig(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
