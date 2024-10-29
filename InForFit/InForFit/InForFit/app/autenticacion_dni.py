from django.contrib.auth import authenticate
from .models import *
def authenticate_dni(dni, password):
    try:
        # Busca el usuario relacionado con el DNI proporcionado
        print(dni)
        print(password)
        socio = DatosDomicilio.objects.get(dni=dni)
        user = socio.user
        # Autentica usando la contraseña del usuario
        if user.check_password(password):
            return user
    except DatosDomicilio.DoesNotExist:
        return None
