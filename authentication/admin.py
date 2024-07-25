from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "email", "phone_number", "user_picture"]
    search_fields = ["username", "email", "phone_number"]

admin.site.register(User, UserAdmin)