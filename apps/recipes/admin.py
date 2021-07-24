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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('usuario','receta','comment')
    list_filter = ('user','recipe')

    def usuario(self, obj):
        return obj.user.username
    
    def receta(self, obj):
        return obj.recipe.title

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('creador','receta','dificultad','tiempo_de_preparacion','created_at')
    list_filter = ('created_by',)

    def creador(self, obj):
        return obj.created_by.username
    
    def receta(self, obj):
        return obj.title
    
    def dificultad(self, obj):
        return obj.get_difficulty_display()

    def tiempo_de_preparacion(self, obj):
        return obj.get_preparation_time_display()

admin.site.register(Step, StepAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Recipe, RecipeAdmin)
