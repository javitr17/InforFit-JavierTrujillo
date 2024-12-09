from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction


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
    imagen = models.ImageField(upload_to='imagenes_socios/', blank=True, null=True)  # Nueva línea

    def __str__(self):
        return f"Usuario: {self.user.username}, Nombre: {self.nombre}, Apellidos: {self.apellidos}"

class DatosFisicos(models.Model):
    user = models.ForeignKey(Socio, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # Peso con decimales
    altura = models.DecimalField(max_digits=3, decimal_places=2)  # Altura en metros, con decimales
    imc = models.DecimalField(max_digits=4, decimal_places=2)  # IMC calculado, con decimales

    def __str__(self):
        return f" {self.user}, IMC: {self.imc}"


class Suscripción(models.Model):
    user = models.ForeignKey(Socio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Nombre de la suscripción
    precio_suscripcion = models.DecimalField(max_digits=6, decimal_places=2)  # Precio de la suscripción
    precio_inscripcion= models.DecimalField(max_digits=6, decimal_places=2)
    duracion = models.CharField(max_length=100)  # Duración en días, por ejemplo
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    proximo_pago=models.DateField()
    vencimiento_notificado = models.BooleanField(default=False)  # Notificación si fue avisado del vencimiento


    def __str__(self):
        return f" {self.user}, Suscripción: {self.nombre}"


class DatosDomicilio(models.Model):
    user = models.ForeignKey(Socio, on_delete=models.CASCADE)
    dni = models.CharField(max_length=9)
    calle = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return f" {self.user}, DNI: {self.dni}, Ciudad: {self.ciudad,}, Calle: {self.calle}"


class TarjetaPago(models.Model):
    user = models.ForeignKey(Socio, on_delete=models.CASCADE)
    token_stripe = models.CharField(max_length=255)  # Token de Stripe
    ult_cuatro_digitos = models.CharField(max_length=4)  # Últimos cuatro dígitos de la tarjeta
    fecha_ven_parcial = models.CharField(max_length=5)  # Fecha de vencimiento en formato MM/AA
    nombre_titular = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.user}"

class ClaseColectiva(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la clase
    capacidad_max = models.IntegerField()  # Capacidad máxima de asistentes

    def __str__(self):
        return f"Clase: {self.nombre}"

class HorarioClase(models.Model):
    clase_colectiva = models.ForeignKey(ClaseColectiva, on_delete=models.CASCADE)  # Relación con la clase
    fecha_clase = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Clase: {self.clase_colectiva}, Horario: {self.hora_inicio}-{self.hora_fin}"


class ReservaClase(models.Model):
    user = models.ForeignKey(Socio, on_delete=models.CASCADE)
    horario_clase = models.ForeignKey(HorarioClase, on_delete=models.CASCADE)  # Relación con el horario de la clase
    fecha_reserva = models.DateField()

    def __str__(self):
        return f" {self.user}, Horario clase: {self.horario_clase}, Fecha reserva: {self.fecha_reserva,}"


class Asistencia(models.Model):
    user = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fecha_asistencia = models.DateField()

    def __str__(self):
        return f" {self.user}, Fecha asistencia: {self.fecha_asistencia}"







