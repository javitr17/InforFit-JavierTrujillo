from django.http import HttpResponse
from django.shortcuts import render
from ..forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils import timezone


@method_decorator(login_required(login_url='login'), name='dispatch')
class index(View):
    template_name = 'index.html'




@method_decorator(login_required(login_url='login'), name='dispatch')
class perfil(TemplateView):
    template_name = 'app/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el socio relacionado con el usuario autenticado
        socio = Socio.objects.filter(user=self.request.user).first()
        if socio:  # Comprobar que el socio existe
            # Datos del socio
            context['nombre'] = socio.nombre.upper()  # Convertir a mayúsculas
            context['apellidos'] = socio.apellidos.upper()  # Convertir a mayúsculas
            context['id'] = socio.id

            # Datos de la suscripción del socio
            suscripcion = Suscripción.objects.filter(user=socio).first()
            if suscripcion:  # Verificar si el socio tiene una suscripción
                context['contrato'] = suscripcion.nombre  # Campo 'nombre' de la suscripción
                context['precio_suscripcion'] = suscripcion.precio_suscripcion
                context['fecha_inicio'] = suscripcion.fecha_inicio.strftime('%d/%m/%Y')  # Formatear fecha
                context['fecha_vencimiento'] = suscripcion.fecha_vencimiento.strftime('%d/%m/%Y')  # Formatear fecha
                context['proximo_pago'] = suscripcion.proximo_pago.strftime('%d/%m/%Y')  # Formatear fecha
            else:
                # Si no hay suscripción, pasar valores vacíos o None
                context['contrato'] = None
                context['precio_suscripcion'] = None
                context['fecha_inicio'] = None
                context['fecha_vencimiento'] = None
                context['proximo_pago'] = None
        else:
            # Si no hay socio asociado al usuario autenticado
            context['nombre'] = None
            context['apellidos'] = None
            context['id'] = None
            context['contrato'] = None
            context['precio_suscripcion'] = None
            context['fecha_inicio'] = None
            context['fecha_vencimiento'] = None
            context['proximo_pago'] = None

        return context

