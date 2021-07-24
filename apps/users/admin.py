from django.contrib import admin
from .models import CustomModelUser, CodeVerification, Follower
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class FollowerAdmin(admin.ModelAdmin):
	list_display = ['user', 'follower','created_at']
	list_filter = ['user']

class CodeVerificationAdmin(admin.ModelAdmin):
	list_display = ['user', 'code', 'created','expiration','used']
	list_filter = ['user','used']

class CustomUserAdmin(UserAdmin):
	edi = list(UserAdmin.fieldsets)
	edi.append(("Perfil", {
		"fields": ('image_profile',)
	}))
	fieldsets = tuple(edi)
	list_display = ['username','first_name','last_name','email','is_staff','is_active']
	list_filter = ['is_staff','is_active']


admin.site.register(CustomModelUser, CustomUserAdmin)
admin.site.register(CodeVerification, CodeVerificationAdmin)
admin.site.register(Follower, FollowerAdmin)


