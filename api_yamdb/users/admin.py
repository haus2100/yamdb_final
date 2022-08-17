from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "bio",
        "role",
    )
    list_editable = ("bio",)
    search_fields = ("bio",)
    list_filter = ("role",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
