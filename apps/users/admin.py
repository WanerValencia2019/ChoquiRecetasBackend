from django.contrib import admin
from .models import CustomModelUser, CodeVerification, Follower
# Register your models here.


class FollowerAdmin(admin.ModelAdmin):
	list_display = ['user', 'follower']

admin.site.register(CustomModelUser);
admin.site.register(CodeVerification);


admin.site.register(Follower, FollowerAdmin);

