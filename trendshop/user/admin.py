from django.contrib import admin
from .models import User,UserAddress


class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user_types",)

admin.site.register(User,UserAdmin)
admin.site.register(UserAddress)