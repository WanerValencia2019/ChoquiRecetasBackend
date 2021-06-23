from rest_framework import serializers

from apps.users.models import CustomModelUser
from apps.users.serializers import UserSerializer
from .models import Recipe, CommentsRecipe, Step

import os, json

User = CustomModelUser


class StepSerializer(serializers.ModelSerializer):
	class Meta:
		model = Step
		fields = '__all__'

class CommentsRecipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentsRecipe
		fields = ['user','comment']

class StepListingField(serializers.RelatedField):
    def to_representation(self, value):
        #duration = time.strftime('%M:%S', time.gmtime(value.duration))
        print(dir(os))
        data = {
        	'id': value.id,
        	'description': value.description,
        	'image':value.image.url
        }
        return json.dumps(data)


class RecipeSerializer(serializers.ModelSerializer):
	created_by = UserSerializer(many=False, read_only=True)
	steps = StepListingField(many=True, read_only=True)
	commentsrecipe_set = CommentsRecipeSerializer(many=True, read_only=True)

	class Meta:
		model = Recipe
		fields=['created_by','title', 'description','ingredients','steps','commentsrecipe_set','created_at']