import logging

import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)


class BrevoEmailError(Exception):
    pass


def _get_transactional_api():
    if not settings.BREVO_API_KEY:
        raise BrevoEmailError('BREVO_API_KEY no está configurada.')

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    configuration.host = 'https://api.brevo.com/v3'
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_email(*, to_email, to_name, subject, html_content, text_content=None, reply_to=None):
    if not settings.BREVO_SENDER_EMAIL:
        raise BrevoEmailError('BREVO_SENDER_EMAIL no está configurada.')

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            'name': settings.BREVO_SENDER_NAME,
            'email': settings.BREVO_SENDER_EMAIL,
        },
        to=[{'email': to_email, 'name': to_name}],
        subject=subject,
        html_content=html_content,
        text_content=text_content or _html_to_text(html_content),
    )

    if reply_to:
        send_smtp_email.reply_to = reply_to

    try:
        api_instance = _get_transactional_api()
        response = api_instance.send_transac_email(send_smtp_email)
        return response
    except ApiException as exc:
        logger.exception('Error al enviar correo con Brevo')
        raise BrevoEmailError(str(exc.body or exc)) from exc
    except Exception as exc:
        logger.exception('Error de conexión al enviar correo con Brevo')
        raise BrevoEmailError(str(exc)) from exc


def send_distributor_request_notification(distributor_request):
    if not settings.BREVO_NOTIFICATION_EMAIL:
        raise BrevoEmailError('BREVO_NOTIFICATION_EMAIL no está configurada.')

    company = distributor_request.company or 'Sin nombre'
    subject = f'Nueva solicitud de distribuidor: {company}'

    html_content = f"""
    <h2>Nueva solicitud de distribuidor</h2>
    <p><strong>Empresa:</strong> {company}</p>
    <p><strong>Contacto:</strong> {distributor_request.contact_name}</p>
    <p><strong>Correo:</strong> {distributor_request.email}</p>
    <p><strong>Teléfono:</strong> {distributor_request.phone}</p>
    <p><strong>Dirección:</strong><br>{distributor_request.company_address}</p>
    <p><strong>Información adicional:</strong><br>{distributor_request.message}</p>
    """

    return send_email(
        to_email=settings.BREVO_NOTIFICATION_EMAIL,
        to_name=settings.BREVO_SENDER_NAME,
        subject=subject,
        html_content=html_content,
        reply_to={
            'email': distributor_request.email,
            'name': distributor_request.contact_name,
        },
    )


def send_test_email():
    return send_email(
        to_email=settings.BREVO_NOTIFICATION_EMAIL,
        to_name=settings.BREVO_SENDER_NAME,
        subject='Prueba de Brevo - Sazonova',
        html_content='<p>Este es un correo de prueba enviado desde el backend de Sazonova.</p>',
    )


def _html_to_text(html_content):
    return (
        html_content.replace('<br>', '\n')
        .replace('<p>', '')
        .replace('</p>', '\n')
        .replace('<h2>', '')
        .replace('</h2>', '\n')
        .replace('<strong>', '')
        .replace('</strong>', '')
    )
