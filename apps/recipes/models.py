from django.db import models
from apps.users.models import CustomModelUser
# Create your models here.


class Step(models.Model):
	description = models.TextField(null=False)
	image = models.ImageField(upload_to="recipes/", null=True, blank=True)

	def __str__(self):
		return self.description


class Recipe(models.Model):
	created_by = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE)
	description = models.TextField(null=False)
	ingredients = models.JSONField(default=[])
	steps = models.ManyToManyField(Step, related_name="recipe_steps")
	likes = models.ManyToManyField(CustomModelUser, related_name="recipe_likes")
	comments = models.ManyToManyField(CustomModelUser, through="CommentsRecipe", related_name="recipe_comments")
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.created_by


class CommentsRecipe(models.Model):
	user = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	comment = models.CharField(verbose_name="Comentario",max_length=300)
	created_at = models.DateTimeField(auto_now_add=True)





