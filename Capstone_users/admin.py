from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender', 'email', 'is_staff', 'is_superuser')
    list_filter = ('username', 'gender', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'gender', 'email', 'is_staff', 'is_superuser')
    list_editable = ['gender', 'email', 'is_staff', 'is_superuser']