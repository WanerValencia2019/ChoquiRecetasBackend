
from django.urls import path
from .api import RecipeView

app_name = 'recipes'

urlpatterns = [
	path('', RecipeView.as_view(), name='detail-recibe')
]