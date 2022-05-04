from django.contrib import admin
from .models import Reviews

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
     list_display = ('user', 'text', 'created_on', 'approved', 'is_active')
     list_filter = ('user',)
     actions = ['set_approved_to_true', 'set_is_active_to_true', 'set_all_attributes_to_true']

     def set_approved_to_true(self, request, queryset):
          queryset.update(approved = True)


     def set_is_active_to_true(self, request, queryset):
          queryset.update(is_active = True)


     def set_all_attributes_to_true(self, request, queryset):
          queryset.update(is_active = True)
          queryset.update(approved = True)