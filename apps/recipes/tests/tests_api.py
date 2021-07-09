import json
import unittest

from django.test import TestCase
from apps.recipes.models import Recipe, Step, CommentsRecipe
from apps.users.models import CustomModelUser

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase 
from rest_framework import status

from apps.utils import get_binary_content
from images import image_principal, step_one_image, step_two_image, fail_image

User = CustomModelUser



class RecipeTestCase(APITestCase):
    def setUp(self):
        self.user = User(is_active=True,username="test_admin", first_name="Tests", last_name="Admin")
        self.user.set_password("test_admin")
        self.user.save()
        Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        data = {
            "title": "Arroz test - 5 personas",
            "description": "Esta es una de las mejores recetas para compartir con amigos y familiares.",
            "image": image_principal,
            "ingredients": [
                "1 libra 1/2 de arroz",
                "Cebolla",
                "Tomate",
                "4 libra de queso",
                "2 libra de queso manchego",
                "1 galon de aceite",
                "200gr de sal",
                "3 tomates de arbol"
            ],
            "steps": [
                {	
                    "description": "Mezclamos la comida y montamos al fogón",
                    "image": step_one_image
                },
                {
                    "description": "Cocinamos con revueltos al gusto",
                    "image": step_two_image
                }
            ]
        }
        image = get_binary_content(data.get('image'))
        self.recipe = Recipe()
        self.recipe.created_by=self.user
        self.recipe.title=data.get('title')
        self.recipe.image.save("name_image.jpeg",image, save=False)
        self.recipe.ingredients = data.get('ingredients')
        self.recipe.description = data.get('description')
        self.recipe.save()
        objs_steps = []
        for step in data.get('steps'):
            obj = Step()
            obj.description = step.get('description')
            file = get_binary_content(step.get('image'))
            #print(file)
            if file is not None:
                obj.image.save("name_image.jpeg",file, save=False)
            objs_steps.append(obj)
        self.recipe.steps.set(self.recipe.steps.bulk_create(objs_steps))
        self.recipe.save()

    def test_create_recipe(self):
        data = {
            "created_by": f"{self.user.uuid}",
            "title": "Arroz test - 5 personas",
            "description": "Esta es una de las mejores recetas para compartir con amigos y familiares.",
            "image": image_principal,
            "ingredients": [
                "1 libra 1/2 de arroz",
                "Cebolla",
                "Tomate",
                "4 libra de queso",
                "2 libra de queso manchego",
                "1 galon de aceite",
                "200gr de sal",
                "3 tomates de arbol"
            ],
            "steps": [
                {	
                    "description": "Mezclamos la comida y montamos al fogón",
                    "image": step_one_image
                },
                {
                    "description": "Cocinamos con revueltos al gusto",
                    "image": step_two_image
                }
            ]
        }
        response_succes = {'message': 'Receta creada satisfactoriamente'}
        response = self.client.post("/api/v1/recipes/create", data, format="json", )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(json.dumps(response_succes), response.data)    
    
    @unittest.expectedFailure
    def test_step_image_error(self):
        data = {
            "created_by": f"{self.user.uuid}",
            "title": "Arroz test - 5 personas",
            "description": "Esta es una de las mejores recetas para compartir con amigos y familiares.",
            "image": fail_image,
            "ingredients": [
                "1 libra 1/2 de arroz",
                "Cebolla",
                "Tomate",
                "4 libra de queso",
                "2 libra de queso manchego",
                "1 galon de aceite",
                "200gr de sal",
                "3 tomates de arbol"
            ],
            "steps": [
                {	
                    "description": "Mezclamos la comida y montamos al fogón",
                    "image": step_one_image
                },
                {
                    "description": "Cocinamos con revueltos al gusto",
                    "image": step_two_image
                }
            ]
        }
        response_succes = {'message': 'Receta creada satisfactoriamente'}
        response = self.client.post("/api/v1/recipes/create", data, format="json", )
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(json.dumps(response_succes), response.data)
           
    def test_detail_recipe(self):
        response = self.client.get(f"/api/v1/recipes/{self.recipe.uuid}",format="json")
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.uuid, response.data['created_by'].get('uuid'))

    def test_user_preview_recipe(self):
        response = self.client.get(f"/api/v1/recipes/user/{self.user.uuid}",format="json")
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.user.uuid, response.data[0]['created_by'].get('uuid'))        

    def test_like_recipe(self):
        data = {
            "user_uuid": self.user.uuid,
            "recipe_uuid": self.recipe.uuid
        }
        response_succes = {'message': 'Operación realizada con éxito'}
        response = self.client.post("/api/v1/recipes/like",data,format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, self.recipe.likes.all().count())
        self.assertJSONEqual(json.dumps(response_succes), response.data)
    
    def test_comment_recipe(self):
        data = {
            "user_uuid": self.user.uuid,
            "recipe_uuid": self.recipe.uuid,
            "comment": "Este es un comentario hecho por el test admin"
        }
        response_succes = {"message":"Comentario creado satisfactoriamente"}
        response = self.client.post("/api/v1/recipes/comment",data,format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(json.dumps(response_succes), response.data)
        self.assertEqual(1, self.recipe.commentsrecipe_set.all().count())
        self.assertEqual(data.get('comment'), self.recipe.commentsrecipe_set.all().first().comment)


