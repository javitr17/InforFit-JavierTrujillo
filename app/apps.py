from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.shortcuts import redirect


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Conectamos la señal post_migrate con la función de verificación
        post_migrate.connect(self.check_suscripciones_inactivas)

    def check_suscripciones_inactivas(self, sender, **kwargs):
        # Realizamos las importaciones aquí para evitar el error de "Apps aren't loaded yet"
        from .models import Socio, Suscripción  # Importamos los modelos aquí

        # Ejecutamos la función de verificación después de las migraciones
        verificar_suscripciones_inactivas(Socio, Suscripción)


def verificar_suscripciones_inactivas(Socio, Suscripción):
    # Obtenemos todos los socios con suscripción inactiva
    socios_inactivos = Suscripción.objects.filter(suscripcion_activa=False)

    # Comprobamos si la fecha de vencimiento coincide con la fecha actual
    for suscripcion in socios_inactivos:
        if suscripcion.fecha_vencimiento.date() == timezone.now().date():
            # Si las fechas coinciden, bloqueamos al socio (cerramos sesión)
            socio = suscripcion.user
            if socio.is_authenticated:
                logout(socio)  # Deslogueamos al socio si está autenticado
                # Opcionalmente, redirigimos a una página que avise sobre la cancelación de la suscripción
                return redirect('welcome')

