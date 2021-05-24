import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .managers import CodeVerificationManager
# Create your models here.


class CustomModelUser(AbstractUser):
	user_outstanding = models.BooleanField(default=False)




class CodeVerification(models.Model):
	user = models.OneToOneField(CustomModelUser, blank=False, null=False, on_delete=models.CASCADE)
	code = models.CharField(verbose_name="Código",max_length=4, blank=True, null=False)
	created = models.DateTimeField(auto_now_add=True)
	expiration = models.DateTimeField(default=timezone.now()+timedelta(minutes=5))
	used = models.BooleanField(default=False)
	objects = CodeVerificationManager()
	



	def __str__(self):
		return f"{self.user} - {self.code}"

@receiver(pre_save, sender=CodeVerification)
def creatCodeVerification(instance,*args, **kwargs):
	code = generateCode()
	if not instance.code:
		instance.code = code




def generateCode():
	digits = "0123456789"
	code = ""
	for i in range(4):
		code += digits[random.randrange(0,10)]

	return code
