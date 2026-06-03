from django.contrib import admin

from .models import Gig, UserProfile


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
	list_display = ('title', 'poster', 'category', 'location', 'price', 'status', 'created_at')
	list_filter = ('category', 'status')
	search_fields = ('title', 'description')
	raw_id_fields = ('poster',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'email', 'phone_number', 'whatsapp_number')
	search_fields = ('user__username', 'email', 'phone_number', 'whatsapp_number')
