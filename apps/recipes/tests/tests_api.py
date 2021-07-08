from django.test import TestCase
from apps.recipes.models import Recipe, Step, CommentsRecipe
from apps.users.models import CustomModelUser

User = CustomModelUser


class RecipeTestCase(TestCase):
    def setUp(self):
        print("Comenzamos el test")

    
    def test_create_recipe(self):
        self.assertEqual("hola","holas")


