from django.contrib import admin
from .models import Reviews

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
     list_display = ('user', 'text', 'created_on', 'approved', 'is_active')
