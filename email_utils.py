import aiosmtplib
from email.message import EmailMessage
from config import settings

async def enviar_email(asunto, cuerpo, reply_to=None):
    mensaje = EmailMessage()
    mensaje["From"] = settings.EMAIL_FROM
    mensaje["To"] = settings.EMAIL_TO
    mensaje["Subject"] = asunto

    if reply_to:
        mensaje["Reply-To"] = reply_to

    mensaje.set_content(cuerpo)

    try:
        await aiosmtplib.send(
            mensaje,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
            start_tls=True,
        )
        return True
    except Exception as e:
        print(f"[ERROR] Fallo el envío de correo: {e}")
        return False
