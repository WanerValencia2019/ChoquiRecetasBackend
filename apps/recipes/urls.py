
from django.urls import path
from . import api

app_name = 'recipes'

urlpatterns = [
	path('create',api.CreateRecipeView.as_view(), name='create-recipe'),
	path('all',api.RecipesView.as_view(), name="all-recipes"),
	path('like',api.LikeRecipeView.as_view(), name='like-recipe'),
	path('comment', api.CommentRecipeView.as_view(), name="comment-recipe"),
	path('<str:uuid>',api.RecipeDetailView.as_view(), name='detail-recipe'),
	path('update/<str:uuid>',api.UpdateRecipeView.as_view(), name='update-recipe'),
	path('user/<str:uuid>',api.UserRecipesView.as_view(), name="user_recipes"),
]