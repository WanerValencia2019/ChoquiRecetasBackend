from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from . import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Recipe

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



class RecipeDetailView(APIView):
	serializer = serializers.RecipeSerializer
	#create_serializer = serializers.CreateRecipeSerializer
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)


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
	serializer_class = serializers.CreateRecipeSerializer
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)

	def post(self, request):
		recipe = self.get_serializer(data=request.data)
		recipe.is_valid(raise_exception=True)
		recipe.save()
		
		return Response({"message":"Receta creada satisfactoriamente"}, status.HTTP_201_CREATED)


class UpdateRecipeView(UpdateAPIView):
	serializer_class = serializers.UpdateRecipeSerializer
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)

	def get_object(self):
		uuid = self.kwargs.get('uuid')
		user_uuid = self.request.user.uuid
		try: 
			recipe = Recipe.objects.get(uuid=uuid, created_by__uuid=user_uuid)
			return recipe
		except ObjectDoesNotExist as ex:
			return None

	def update(self, request, *args, **kwargs):	
		recipe = self.get_object()
		uuid = self.kwargs.get('uuid')
		if recipe is None:
			return Response({"message":"Esta receta no ha sido creada"}, status.HTTP_400_BAD_REQUEST)

		serialized = self.get_serializer(data=request.data)
		serialized.is_valid(raise_exception=True)
		serialized.save(uuid=uuid)
		#print(serialized.data)

		return Response({"message":"Receta actualizada éxitosamente"}, status.HTTP_200_OK)

	

class LikeRecipeView(GenericAPIView):
	serializer_class = serializers.LikeRecipeSerializer
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		return Response({"message":"Operación realizada con éxito"}, status.HTTP_201_CREATED)


class UserRecipesView(ListAPIView):
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)
	serializer_class = serializers.RecipeSerializer

	def get_queryset(self):
		recipes = Recipe.objects.filter(created_by__uuid=self.kwargs.get('uuid')).select_related('created_by').prefetch_related('likes','comments','steps')
		if len(recipes) != 0:
			return recipes
		return None

	def list(self, request, *args, uuid):
		objs = self.get_queryset()
		recipes_serialized = self.get_serializer(instance=objs, many=True)
		data = recipes_serialized.data

		return Response(data, status.HTTP_200_OK)


class UserPreviewRecipesView(ListAPIView):
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)
	serializer_class = serializers.PreviewRecipeSerializer

	def get_queryset(self):
		recipes = Recipe.objects.filter(created_by__uuid=self.kwargs.get('uuid')).select_related('created_by').prefetch_related('likes','comments','steps')
		if len(recipes) != 0:
			return recipes
		return None

	def list(self, request, *args, uuid):
		objs = self.get_queryset()
		recipes_serialized = self.get_serializer(instance=objs, many=True)
		data = recipes_serialized.data
		return Response(data, status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    #max_page_size = 1000


class RecipesView(ListAPIView):
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)
	queryset = Recipe.objects.all().select_related('created_by').prefetch_related('likes','comments','steps')
	serializer_class = serializers.RecipeSerializer
	#pagination_class = StandardResultsSetPagination

class CommentRecipeView(GenericAPIView):
	serializer_class = serializers.CommentRecipeSerializer
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)

	def validate_user(self, user_uuid):
		if self.request.user.uuid.strip() == user_uuid.strip():
			return True
		return False

	def post(self, request, *args, **kwargs):
		user_uuid = request.data.get('user_uuid')

		if not self.validate_user(user_uuid):
			return Response({"message":"Usuario no verificado"}, status.HTTP_400_BAD_REQUEST)
		serialized = self.get_serializer(data=request.data)
		serialized.is_valid(raise_exception=True)
		serialized.save()
		return Response({"message":"Comentario creado satisfactoriamente"}, status.HTTP_201_CREATED)





