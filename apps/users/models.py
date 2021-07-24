import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .managers import CodeVerificationManager
# Create your models here.


def path_to_rename(instance, filename):
	extension = filename.split(".")[-1]
	name = uuid.uuid4().hex
	return f"profiles/{name}.{extension}"




class CustomModelUser(AbstractUser):
	uuid = models.CharField(max_length=40, null=True, blank=True, )
	user_outstanding = models.BooleanField(default=False)
	image_profile = models.ImageField(verbose_name="Imagén de perfil", upload_to=path_to_rename,null=True, blank=True)
    
	def __str__(self):
		return f"{self.username}"

@receiver(pre_save,sender=CustomModelUser)
def set_uuid(instance, *args, **kwargs):
	if not instance.uuid:
		instance.uuid = uuid.uuid4().hex


class Follower(models.Model):
	user = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE, blank=True,null=True, related_name="user_followed")
	follower = models.ForeignKey(CustomModelUser, on_delete=models.CASCADE, blank=True, null=True, related_name="user_follower")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user} - {self.follower}"

	class Meta:
		verbose_name = "Seguidor"
		verbose_name_plural = "Seguidores"
		ordering = ['-created_at']

class CodeVerification(models.Model):
	user = models.OneToOneField(CustomModelUser, blank=False, null=False, on_delete=models.CASCADE)
	code = models.CharField(verbose_name="Código",max_length=4, blank=True, null=False)
	created = models.DateTimeField(auto_now_add=True)
	expiration = models.DateTimeField(verbose_name="Fecha de expiración",blank=True,null=False)
	used = models.BooleanField(default=False)
	objects = CodeVerificationManager()
	
	class Meta:
		verbose_name = "Código de verificación"
		verbose_name_plural = "Códigos de verificación"
		ordering = ['-created']

	def __str__(self):
		return f"{self.user} - {self.code}"

@receiver(pre_save, sender=CodeVerification)
def creatCodeVerification(instance,*args, **kwargs):
	code = generateCode()
	if not instance.code:
		instance.code = code

	if not instance.expiration:
		instance.expiration = timezone.now()+timedelta(minutes=5)



def generateCode():
	digits = "0123456789"
	code = ""
	for i in range(4):
		code += digits[random.randrange(0,10)]

	return code
