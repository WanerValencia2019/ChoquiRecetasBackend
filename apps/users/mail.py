from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class Mail():
    @staticmethod
    def send_code_verification(user, code):
        subject = 'Código de verificación <ChoquiRecetas>'
        template = get_template('mail.html')
        content = template.render({
            'user':user,
            'codeVerification':code
        })

        message = EmailMultiAlternatives(subject, content,settings.EMAIL_HOST_USER, to=[user.email])
        message.content_subtype="html"
        message.send()

    @staticmethod
    def send_reseted_password(user, password):
        subject = 'Restablecimiento de contraseña <ChoquiRecetas>'
        template = get_template('mail_reset_password.html')
        content = template.render({
            'user':user,
            'password': password
        })

        message = EmailMultiAlternatives(subject, content,settings.EMAIL_HOST_USER, to=[user.email])
        message.content_subtype="html"
        message.send()

