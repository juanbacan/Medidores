
import threading
import random
import string
from django.core.mail import send_mail

def enviar_correo_electronico_asincrono(asunto, mensaje, destinatarios, remitente=None):
    def enviar_correo():
        send_mail(asunto, mensaje, remitente, destinatarios)

    # Creamos un hilo y ejecutamos la función enviar_correo en ese hilo
    correo_thread = threading.Thread(target=enviar_correo)
    correo_thread.start()


def generar_contrasena(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for i in range(longitud))
    return contrasena