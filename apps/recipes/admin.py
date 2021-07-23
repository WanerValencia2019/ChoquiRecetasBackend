from django.contrib import admin
from .models import Recipe, Comment, Step
# Register your models here.


class StepAdmin(admin.ModelAdmin):
    list_display = ['description',]


admin.site.register(Step, StepAdmin)
admin.site.register(Recipe)
admin.site.register(Comment)