from django.db import models
from apps.users.models import CustomModelUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
# Create your models here.
from apps.utils import PreparationTime, Difficulty

def path_to_rename(instance, filename):
	extension = filename.split(".")[-1]
	name = uuid.uuid4().hex
	return f"recipes/{name}.{extension}"

	def __str__(self):
		return self.description

class Recipe(models.Model):
	uuid = models.CharField(max_length=40, null=True, blank=True, )
	created_by = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=200,null=False,default="")
	description = models.TextField(null=False)
	image = models.ImageField(verbose_name="Imagen descriptiva",upload_to=path_to_rename,null=False, blank=True)
	ingredients = models.JSONField(default=list())
	preparation_time = models.CharField(max_length=6, choices=[x.value for x in PreparationTime], default=PreparationTime.SHORT)
	difficulty = models.CharField(max_length=6, choices=[x.value for x in Difficulty], default=Difficulty.EASY)
	likes = models.ManyToManyField(CustomModelUser, related_name="recipe_likes", blank=True)	
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.title}"
	class Meta:
		verbose_name = "Receta"
		verbose_name_plural = "Recetas"
		ordering = ['-created_at']


@receiver(pre_save,sender=Recipe)
def set_uuid(instance, *args, **kwargs):
	if not instance.uuid:
		instance.uuid = uuid.uuid4().hex

class Comment(models.Model):
	user = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	comment = models.CharField(verbose_name="Comentario",max_length=300)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.recipe.title}"

	class Meta:
		verbose_name = "Comentario"
		verbose_name_plural = "Comentarios"
		ordering = ['user__id']
		

class Step(models.Model):
	recipe=models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Receta")
	description = models.TextField(null=False, verbose_name="Descripción")
	image = models.ImageField(upload_to=path_to_rename, null=False, blank=False, verbose_name="Imagen descriptiva")
	number = models.PositiveIntegerField(default=1, verbose_name="#")

	def __str__(self):
		return f"{self.recipe.title} - {self.recipe.title}"

	class Meta:
		verbose_name = "Paso"
		verbose_name_plural = "Pasos"
		ordering = ['recipe__id','number']
