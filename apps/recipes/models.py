from django.db import models
from apps.users.models import CustomModelUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
# Create your models here.


def path_to_rename(instance, filename):
	extension = filename.split(".")[-1]
	name = uuid.uuid4().hex
	return f"recipes/{name}.{extension}"

class Step(models.Model):
	description = models.TextField(null=False)
	image = models.ImageField(upload_to=path_to_rename, null=True, blank=True)

	def __str__(self):
		return self.description


class Recipe(models.Model):
	uuid = models.CharField(max_length=40, null=True, blank=True, )
	created_by = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=200,null=False,default="")
	description = models.TextField(null=False)
	image = models.ImageField(verbose_name="Imagen descriptiva",upload_to=path_to_rename,null=False, blank=True)
	ingredients = models.JSONField(default=[])
	steps = models.ManyToManyField(Step, related_name="recipe_steps")
	likes = models.ManyToManyField(CustomModelUser, related_name="recipe_likes", null=True)
	comments = models.ManyToManyField(CustomModelUser, through="CommentsRecipe", related_name="recipe_comments")
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.title} - {self.created_by.username} - {self.uuid}"


@receiver(pre_save,sender=Recipe)
def set_uuid(instance, *args, **kwargs):
	if not instance.uuid:
		instance.uuid = uuid.uuid4().hex

class CommentsRecipe(models.Model):
	user = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	comment = models.CharField(verbose_name="Comentario",max_length=300)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.recipe.title}"





