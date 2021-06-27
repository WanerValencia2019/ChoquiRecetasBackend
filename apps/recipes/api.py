from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication 

from .serializers import RecipeSerializer, CreateRecipeSerializer
from .models import Recipe
from django.core.files.storage import Storage
from django.core.files import File
from django.core.files.base import ContentFile
import base64
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening



def handle_uploaded_file(filename):
	name = filename.split('/')[-1].split('.')[0]
	ext = filename.split('/')[-1].split('.')[-1]
	#print(name, ext)
	with open(f"./{name}.{ext}", "wb") as destination:
			destination.write(f)



class RecipeView(APIView):
	serializer = RecipeSerializer
	create_serializer = CreateRecipeSerializer
	authentication_classes=(CsrfExemptSessionAuthentication,)



	def get(self, request, format=None):
		recipe = Recipe.objects.all().first()
		recipe_serialized = self.serializer(instance=recipe, context={"request":request})
		data={}
		data = recipe_serialized.data
		#print("Holaaa")
		return Response(data, status.HTTP_200_OK)

	def post(self, request):
		steps = request.data['steps'][0]
		image = steps.get('image')
		recipe = self.create_serializer(data=request.data)
		recipe.is_valid(raise_exception=True)
		recipe.save()
		
		return Response({"message":"Receta creada satisfactoriamente"}, status.HTTP_200_OK)