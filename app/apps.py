from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.shortcuts import redirect
from django.core.management import execute_from_command_line



class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Conectamos la señal post_migrate con la función de verificación
        post_migrate.connect(self.check_suscripciones_inactivas)

    def check_suscripciones_inactivas(self, sender, **kwargs):
        # Verificar si estamos en el contexto de migración
        if kwargs.get('using') == 'default':  # Solo ejecuta si estamos en la base de datos principal
            return  # Salimos sin ejecutar lógica
        # Realizamos las importaciones aquí para evitar el error de "Apps aren't loaded yet"
        from .models import Socio, Suscripción  # Importamos los modelos aquí



def verificar_suscripciones_inactivas(Socio, Suscripción):
    # Obtenemos todos los socios con suscripción inactiva
    for suscripcion in Suscripción.objects.all():
        # Verificar si fecha_vencimiento no es None antes de acceder a .date()
        if suscripcion.fecha_vencimiento and suscripcion.fecha_vencimiento.date() == timezone.now().date():
            # Si las fechas coinciden, bloqueamos al socio (cerramos sesión)
            socio = suscripcion.user
            if socio.is_authenticated:
                logout(socio)  # Deslogueamos al socio si está autenticado
                # Opcionalmente, redirigimos a una página que avise sobre la cancelación de la suscripción
                return redirect('welcome')

