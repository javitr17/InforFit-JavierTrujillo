from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Socio)
admin.site.register(Suscripción)
admin.site.register(DatosFisicos)
admin.site.register(DatosDomicilio)
admin.site.register(TarjetaPago)
admin.site.register(ClaseColectiva)
admin.site.register(HorarioClase)
admin.site.register(ReservaClase)
admin.site.register(Asistencia)