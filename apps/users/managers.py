from django.utils import timezone
from django.db.models import Manager, Q





class CodeVerificationManager(Manager):
	def verify_code(self, email, code):
		codeVerification = self.filter(Q(user__email = email) & Q(code = code) & 
    		Q(expiration__gte=timezone.now()) & Q(used = False))

		if len(codeVerification) != 0:
			return codeVerification.first()

		return None

	def create_code_verification(self, User, email):
		user = User.objects.filter(email=email).first()

		if user != None:
			try:
				code = self.get(user=user).delete()
				codeVerification = self.create(user=user)
				return codeVerification
			except:
				codeVerification = self.create(user=user)
				return codeVerification

		return None



