from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication 

from .serializers import RecipeSerializer, CreateRecipeSerializer, LikeRecipeSerializer
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


	def get(self, request, format=None, uuid=None):
		recipe = Recipe.objects.filter(uuid=uuid).first()
		if recipe is None:
			return Response({"message":"Esta receta no existe"}, status.HTTP_400_BAD_REQUEST)
		recipe_serialized = self.serializer(instance=recipe, context={"request":request})
		data={}
		data = recipe_serialized.data
		#print("Holaaa")
		return Response(data, status.HTTP_200_OK)


class CreateRecipeView(GenericAPIView):
	serializer_class = CreateRecipeSerializer
	authentication_classes=(CsrfExemptSessionAuthentication,)

	def post(self, request):
		recipe = self.get_serializer(data=request.data)
		recipe.is_valid(raise_exception=True)
		recipe.save()
		
		return Response({"message":"Receta creada satisfactoriamente"}, status.HTTP_200_OK)



class LikeRecipeView(GenericAPIView):
	serializer_class = LikeRecipeSerializer
	authentication_classes=(CsrfExemptSessionAuthentication,)

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		return Response({"message":"Operación realizada con éxito"}, status.HTTP_200_OK)

