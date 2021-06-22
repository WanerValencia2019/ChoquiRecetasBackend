from django.contrib import admin
from .models import Recipe, CommentsRecipe, Step
# Register your models here.

admin.site.register(Step)
admin.site.register(Recipe)
admin.site.register(CommentsRecipe)