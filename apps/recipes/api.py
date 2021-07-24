from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.decorators import action
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

class RecipeView(ViewSet):
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)
	lookup_field = "uuid"
	queryset = Recipe.objects.all().select_related('created_by').prefetch_related('likes')

	def get_queryset(self):
		uuid = self.kwargs.get('uuid')
		return Recipe.objects.filter(uuid=uuid).first()

	def get_object(self):
		uuid = self.kwargs.get('uuid')
		user_uuid = self.request.user.uuid
		try: 
			recipe = Recipe.objects.get(uuid=uuid, created_by__uuid=user_uuid)
			return recipe
		except ObjectDoesNotExist as ex:
			return None

	def list(self, request, *args, **kwargs):
		serialized = serializers.RecipeSerializer(self.queryset, many=True, context={"request":request})
		data = serialized.data
		return Response(data, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):
		recipe = serializers.CreateRecipeSerializer(data=request.data)
		recipe.is_valid(raise_exception=True)
		recipe.save()
		return Response({"message":"Receta creada satisfactoriamente"}, status.HTTP_201_CREATED)

	def retrieve(self, request,format=None, uuid=None):
		recipe = self.get_queryset()
		if recipe is None:
			return Response({"message":"Esta receta no existe"}, status.HTTP_400_BAD_REQUEST)
		recipe_serialized = serializers.RecipeSerializer(instance=recipe, context={"request":request})
		data={}
		data = recipe_serialized.data
		return Response(data, status.HTTP_200_OK)
	
	def update(self, request, *args, **kwargs):	
		recipe = self.get_object()
		uuid = self.kwargs.get('uuid')
		if recipe is None:
			return Response({"message":"Esta receta no ha sido creada"}, status.HTTP_400_BAD_REQUEST)

		serialized = serializers.UpdateRecipeSerializer(data=request.data)
		serialized.is_valid(raise_exception=True)
		serialized.save(uuid=uuid)
		#print(serialized.data)

		return Response({"message":"Receta actualizada éxitosamente"}, status.HTTP_200_OK)

	@action(methods=['post'],detail=True, url_name="like")
	def like(self, request, *args, **kwargs):
		recipe = self.get_queryset()	
		if recipe is None:
			return Response({"message":"Esta receta no existe"},status.HTTP_200_OK)
		
		serialized = serializers.LikeRecipeSerializer(instance=recipe, data={}, context={"request":self.request})
		serialized.is_valid(raise_exception=True)
		serialized.save()
		return Response({"message":"Operación realizada con éxito"}, status.HTTP_204_NO_CONTENT)

	@action(methods=['post'],detail=True, url_name="comment",)
	def comment(self, request, *args, **kwargs):
		recipe = self.get_queryset()
		comment = self.request.data.get('comment')
		if recipe is None:
			return Response({"message":"Esta receta no existe"},status.HTTP_200_OK)

		serialized = serializers.CommentRecipeSerializer(data={"comment":comment},context={"request":self.request, "recipe":recipe})
		serialized.is_valid(raise_exception=True)
		serialized.save()
		return Response({"message":"Comentario creado satisfactoriamente"}, status.HTTP_201_CREATED)	
	
class UserRecipesView(ListAPIView):
	permission_classes=(IsAuthenticated,)
	authentication_classes=(CsrfExemptSessionAuthentication, TokenAuthentication)
	serializer_class = serializers.RecipeSerializer

	def get_queryset(self):
		recipes = Recipe.objects.filter(created_by__uuid=self.kwargs.get('uuid')).select_related('created_by').prefetch_related('likes')
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






