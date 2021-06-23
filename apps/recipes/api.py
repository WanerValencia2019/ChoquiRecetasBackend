from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication 

from .serializers import RecipeSerializer
from .models import Recipe

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening



class RecipeView(APIView):
	serializer = RecipeSerializer
	authentication_classes=(CsrfExemptSessionAuthentication,)

	def get(self, request, format=None):
		recipe = Recipe.objects.all().first()
		print(dir(recipe))
		recipe_serialized = self.serializer(instance=recipe)
		#print(recipe_serialized.data)
	
		data = recipe_serialized.data
		return Response(data, status.HTTP_200_OK)