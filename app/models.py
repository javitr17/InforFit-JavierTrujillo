from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

class Socio(models.Model):
    genero = models.CharField(
        max_length=10,
        choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro')],
        default='Otro'
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)  # Teléfono como cadena, puede ajustarse el max_length
    email = models.EmailField()

class DatosFisicos(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # Peso con decimales
    altura = models.DecimalField(max_digits=3, decimal_places=2)  # Altura en metros, con decimales
    imc = models.DecimalField(max_digits=4, decimal_places=2)  # IMC calculado, con decimales

class Suscripción(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Nombre de la suscripción
    precio = models.DecimalField(max_digits=6, decimal_places=2)  # Precio de la suscripción
    duracion = models.IntegerField()  # Duración en días, por ejemplo
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    vencimiento_notificado = models.BooleanField(default=False)  # Notificación si fue avisado del vencimiento

class DatosDomicilio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.CharField(max_length=9)
    calle = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=50)

class TarjetaPago(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_stripe = models.CharField(max_length=255)  # Token de Stripe
    ult_cuatro_digitos = models.CharField(max_length=4)  # Últimos cuatro dígitos de la tarjeta
    fecha_ven_parcial = models.CharField(max_length=5)  # Fecha de vencimiento en formato MM/AA
    nombre_titular = models.CharField(max_length=100)

class ClaseColectiva(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la clase
    capacidad_max = models.IntegerField()  # Capacidad máxima de asistentes

class HorarioClase(models.Model):
    id_clase = models.ForeignKey(ClaseColectiva, on_delete=models.CASCADE)  # Relación con la clase
    fecha_clase = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

class ReservaClase(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_horario_clase = models.ForeignKey(HorarioClase, on_delete=models.CASCADE)  # Relación con el horario de la clase
    fecha_reserva = models.DateField()

class Asistencia(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_asistencia = models.DateField()






