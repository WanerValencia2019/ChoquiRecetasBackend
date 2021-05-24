from django.contrib import admin
from .models import CustomModelUser, CodeVerification
# Register your models here.


admin.site.register(CustomModelUser);
admin.site.register(CodeVerification);

