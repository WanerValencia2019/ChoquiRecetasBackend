
from django.urls import path
from .api import RecipeView, LikeRecipeView, CreateRecipeView

app_name = 'recipes'

urlpatterns = [
	path('<str:uuid>/', RecipeView.as_view(), name='detail-recipe'),
	path('create', CreateRecipeView.as_view(), name='create-recipe'),
	path('like', LikeRecipeView.as_view(), name='like-recipe'),
]