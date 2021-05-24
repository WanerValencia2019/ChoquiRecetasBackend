from django.utils import timezone
from django.db.models import Manager, Q





class CodeVerificationManager(Manager):
	def verify_code(self, email, code):
		codeVerification = self.filter(Q(user__email = email) & Q(code = code) & 
    		Q(expiration__gte=timezone.now()) & Q(used = False))

		if len(codeVerification) != 0:
			return codeVerification.first()

		return None


