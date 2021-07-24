from rest_framework import serializers

from apps.users.models import CustomModelUser
#from apps.users.serializers import UserSerializer
from apps.utils import get_binary_content

from .models import Recipe, Comment, Step
from apps.utils import Difficulty, PreparationTime

from django.core.files.base import ContentFile


import os
import json
import base64
import tempfile
import uuid
User = CustomModelUser


class UserRecipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['uuid','username','first_name','last_name','image_profile']
		read_only_fields = ['username']

class StepSerializer(serializers.ModelSerializer):
	class Meta:
		model = Step		
		exclude = ["recipe"]

class CommentsRecipeSerializer(serializers.ModelSerializer):
	user = UserRecipeSerializer(many=False, read_only=True)
	class Meta:
		model = Comment
		fields = ['user','comment']

class StepListingField(serializers.RelatedField):
    def to_representation(self, value):
        #duration = time.strftime('%M:%S', time.gmtime(value.duration))
        #print(dir(os))
        data = {
        	'id': value.id,
        	'description': value.description,
        	'image':value.image.url
        }
        return json.dumps(data)


class PreviewRecipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recipe
		fields=['uuid','created_by','title','image', 'likes']


class RecipeSerializer(serializers.ModelSerializer):
	created_by = UserRecipeSerializer(many=False, read_only=True)
	step = StepSerializer(many=True, read_only=True, source="step_set")
	likes =UserRecipeSerializer(many=True, read_only=True)
	comment = CommentsRecipeSerializer(many=True, read_only=True, source="comment_set")
	class Meta:
		model = Recipe
		fields=['uuid','created_by','title','description','image','ingredients','step','preparation_time','difficulty','comment','likes','created_at']

def get_file_content(url):
	try:
		file = open(url, "rb")
		return file
	except:
		return None


def get_file_name(filename):
	name = filename.split('/')[-1].split('.')[0]
	ext = filename.split('/')[-1].split('.')[-1]

	return name, ext

class CreateRecipeSerializer(serializers.Serializer):
	id=serializers.ReadOnlyField()
	created_by = serializers.CharField(max_length=40, required=True)
	title = serializers.CharField(max_length=200, required=True)
	image = serializers.CharField(required=True)
	steps = serializers.JSONField(default=[])
	description = serializers.CharField(required=True)
	ingredients = serializers.JSONField(default=[])
	preparation_time = serializers.ChoiceField(choices=[x.value for x in PreparationTime], default=PreparationTime.SHORT)
	difficulty = serializers.ChoiceField(choices=[x.value for x in Difficulty], default=Difficulty.EASY)

	def create(self, validated_data):
		name_image = "default.jpeg"	
		created_by = validated_data.get('created_by')
		steps = validated_data.get('steps')
		title = validated_data.get('title')
		description = validated_data.get('description')
		ingredients = validated_data.get('ingredients')
		preparation_time = validated_data.get('preparation_time')
		difficulty = validated_data.get('difficulty')
		image = get_binary_content(validated_data.get('image'))
		

		user = User.objects.filter(uuid=created_by).first()

		recipe = Recipe()
		recipe.created_by = user
		recipe.title = title
		recipe.image.save(name_image,image, save=False)
		recipe.ingredients = ingredients
		recipe.description = description
		recipe.preparation_time = preparation_time
		recipe.difficulty = difficulty
		recipe.save()
		objs_steps = []
		for step in steps:
			obj = Step()
			obj.recipe = recipe
			obj.description = step.get('description')
			obj.number = step.get('number')
			file = get_binary_content(step.get('image'))
			#print(file)
			if file is not None:
				obj.image.save(name_image,file, save=False)
			objs_steps.append(obj)
		recipe.step_set.bulk_create(objs_steps)

		recipe.save()

		return recipe

	def validate(self, data):
		created_by = data.get('created_by')
		steps = data.get('steps')
		title = data.get('title')
		description = data.get('description')
		ingredients = data.get('ingredients')
		image = data.get('image')
		user = User.objects.filter(uuid=created_by).first()

		if len(image)%4 != 0:
			raise serializers.ValidationError({"message":"La imagen no es válida"})

		if user is None:
			raise serializers.ValidationError({"message":"Este usuario no existe"})
		#print(created_by, steps)
		return data

class UpdateRecipeSerializer(serializers.Serializer):
	#id=serializers.ReadOnlyField()
	title = serializers.CharField(max_length=200, required=True)
	description = serializers.CharField(required=True)
	image = serializers.CharField(required=True)
	steps = serializers.JSONField(default=[])
	preparation_time = serializers.ChoiceField(choices=[x.value for x in PreparationTime], default=PreparationTime.SHORT)
	difficulty = serializers.ChoiceField(choices=[x.value for x in Difficulty], default=Difficulty.EASY)
	ingredients = serializers.JSONField(default=[])

	def create(self, validated_data):
		steps = validated_data.get('steps')
		title = validated_data.get('title')
		description = validated_data.get('description')
		ingredients = validated_data.get('ingredients')
		image = get_binary_content(validated_data.get('image'))
		uuid = validated_data.get('uuid')
		preparation_time = validated_data.get('preparation_time')
		difficulty = validated_data.get('difficulty')
		objs_steps = []
		recipe = Recipe.objects.filter(uuid=uuid).first()
		recipe.title=title
		recipe.description=description
		recipe.ingredients=ingredients
		recipe.preparation_time = preparation_time
		recipe.difficulty = difficulty
		recipe.image.save("default.jpeg", image, save=False)
		recipe.save()		
		for step in steps:
			obj = Step.objects.filter(id=step.get('id')).first()
			if obj is None:
				file = get_binary_content(step.get('image'))
				obj = Step()
				obj.recipe = recipe
				obj.description = step.get('description')
				obj.number = step.get('number')		
				if file is not None:
					obj.image.save("default.jpeg", file, save=False)
				obj.save()
				objs_steps.append(obj)
			else:				
				obj.description = step.get('description')
				file = get_binary_content(step.get('image'))
				#print(file)
				if file is not None:
					obj.image.save("default.jpeg", file, save=False)
				objs_steps.append(obj)
		Step.objects.bulk_update(objs_steps, ['description','image'])		
		return recipe

	def validate(self, data):
		steps = data.get('steps')
		title = data.get('title')
		description = data.get('description')
		ingredients = data.get('ingredients')
		image = data.get('image')		

		if len(image)%4 != 0:
			raise serializers.ValidationError({"message":"La imagen no es válida"})
		return data

	def validate_steps(self, value):
		for count,step in enumerate(value, 1):
			image_encoded = step.get('image')
			if len(image_encoded)%4 != 0:
				raise serializers.ValidationError({"message":f"La imagen no es válida en el - paso #{count}"})
				break

		return value


class LikeRecipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recipe
		fields = ["likes"]

	def update(self, recipe, data=None):
		user = self.context['request'].user
		if recipe.likes.filter(id=user.id).exists():		
			recipe.likes.remove(user)
		else:
			recipe.likes.add(user)
		recipe.save()
		return recipe

class CommentRecipeSerializer(serializers.Serializer):
	#recipe_uuid = serializers.CharField(max_length=42)
	#user_uuid = serializers.CharField(max_length=42)
	comment  = serializers.CharField(required=True)

	def create(self, validated_data):
		recipe = self.context['recipe']
		user = self.context['request'].user
		comment = validated_data.get('comment')
		comment = Comment.objects.create(user=user, recipe=recipe,comment=comment)

		return comment

