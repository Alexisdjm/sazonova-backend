from django.core.management.base import BaseCommand

from api.services.brevo import BrevoEmailError, send_test_email


class Command(BaseCommand):
    help = 'Envía un correo de prueba usando Brevo.'

    def handle(self, *args, **options):
        try:
            response = send_test_email()
            message_id = getattr(response, 'message_id', response)
            self.stdout.write(self.style.SUCCESS(f'Correo enviado correctamente. message_id: {message_id}'))
        except BrevoEmailError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
