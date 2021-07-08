
from django.urls import path
from .api import RecipeDetailView, LikeRecipeView, CreateRecipeView, UserRecipesView, RecipesView, UpdateRecipeView

app_name = 'recipes'

urlpatterns = [
	path('all',RecipesView.as_view(), name="all-recipes"),
	path('<str:uuid>', RecipeDetailView.as_view(), name='detail-recipe'),
	path('create', CreateRecipeView.as_view(), name='create-recipe'),
	path('update/<str:uuid>', UpdateRecipeView.as_view(), name='update-recipe'),
	path('like', LikeRecipeView.as_view(), name='like-recipe'),
	path('user/<str:uuid>', UserRecipesView.as_view(), name="user_recipes")
]