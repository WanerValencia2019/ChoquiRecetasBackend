
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api

app_name = 'recipes'

router = DefaultRouter()
router.register('', api.RecipeView, basename="recipes")

urlpatterns = [
	path('user/<str:uuid>',api.UserRecipesView.as_view(), name="user_recipes"),
]

urlpatterns += router.urls