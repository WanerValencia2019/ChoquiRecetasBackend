from django.contrib import admin
from .models import Recipe, Comment, Step
# Register your models here.


class StepAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,{
            "fields":("number","recipe","description")
        }),
        ("Archivos",{
            "fields":("image",)
        })
    )
    list_display = ['recipe','number','description','image']
    list_filter = ['recipe']
    #radio_fields = {'recipe':admin.HORIZONTAL}
    search_fields = ('description','recipe__title')


admin.site.register(Step, StepAdmin)
admin.site.register(Recipe)
admin.site.register(Comment)