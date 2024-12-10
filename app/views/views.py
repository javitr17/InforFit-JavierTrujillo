from django.http import HttpResponse
from django.shortcuts import render
from ..forms import *
from django.urls import reverse
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
        socio = Socio.objects.filter(user=self.request.user).first()

        if socio:
            # Crear formulario con los datos del socio
            form_datos = FormRegistro(instance=socio)
            domicilio = socio.datosdomicilio_set.first()
            if domicilio:
                print(f"Datos de Domicilio: {domicilio.dni}, {domicilio.calle}")
            else:
                print("No hay domicilio asociado al socio.")
            form_domicilio = FormRegistro(instance=socio.datosdomicilio_set.first())  # Obtiene el primer objeto de DatosDomicilio relacionado
            print(f'FOMR DATOS: {form_datos}')
            print(f'FOMR DOMICILIO: {form_domicilio}')
            # DATOS SOCIO
            form_datos.fields['dni'].required = False
            form_datos.fields['calle'].required = False
            form_datos.fields['ciudad'].required = False
            form_datos.fields['codigo_postal'].required = False
            form_datos.fields['pais'].required = False
            form_datos.fields['password'].required = False
            form_datos.fields['password_confirm'].required = False

            # DATOS DOMICILIO
            form_domicilio.fields['nombre'].required = False
            form_domicilio.fields['apellidos'].required = False
            form_domicilio.fields['fecha_nacimiento'].required = False
            form_domicilio.fields['telefono'].required = False
            form_domicilio.fields['email'].required = False
            form_domicilio.fields['genero'].required = False
            form_domicilio.fields['password'].required = False
            form_domicilio.fields['password_confirm'].required = False

            # Agregar datos adicionales del socio y su suscripción al contexto
            context['form_datos'] = form_datos
            context['form_domicilio'] = form_domicilio
            context['nombre'] = socio.nombre.upper()
            context['apellidos'] = socio.apellidos.upper()
            context['id'] = socio.id

            # Obtener la suscripción y agregarla al contexto
            suscripcion = Suscripción.objects.filter(user=socio).first()
            if suscripcion:
                context['contrato'] = suscripcion.nombre
                context['precio_suscripcion'] = suscripcion.precio_suscripcion
                context['fecha_inicio'] = suscripcion.fecha_inicio.strftime('%d/%m/%Y')
                context['fecha_vencimiento'] = suscripcion.fecha_vencimiento.strftime('%d/%m/%Y')
                context['proximo_pago'] = suscripcion.proximo_pago.strftime('%d/%m/%Y')
            else:
                context['contrato'] = None
                context['precio_suscripcion'] = None
                context['fecha_inicio'] = None
                context['fecha_vencimiento'] = None
                context['proximo_pago'] = None
        else:
            messages.error(self.request, "No se encontró un socio asociado al usuario.")
            return redirect('perfil')

        return context

    def post(self, request, *args, **kwargs):
        socio = Socio.objects.filter(user=request.user).first()
        if not socio:
            messages.error(request, "No se encontró un socio asociado al usuario.")
            return redirect('perfil')

        form_datos = FormRegistro(request.POST, instance=socio)

        # Excluir los campos no deseados de la validación
        for campo in ['dni', 'calle', 'ciudad', 'codigo_postal', 'pais', 'password', 'password_confirm']:
            if campo in form_datos.fields:
                form_datos.fields[campo].required = False

        if form_datos.is_valid():
            # Guardar los datos personales
            socio.nombre = form_datos.cleaned_data['nombre']
            socio.apellidos = form_datos.cleaned_data['apellidos']
            socio.telefono = form_datos.cleaned_data['telefono']
            socio.email = form_datos.cleaned_data['email']
            socio.fecha_nacimiento = form_datos.cleaned_data['fecha_nacimiento']
            socio.genero = form_datos.cleaned_data['genero']
            socio.save()

            messages.success(request, "Tus datos personales se han actualizado correctamente.")
            return redirect(reverse('perfil'))

        # Si se actualizan los datos domiciliarios
        form_domicilio = FormRegistro(request.POST, instance=socio.datosdomicilio_set.first())
        if form_domicilio.is_valid():
            # Guardar los datos domiciliarios
            datos_domicilio = form_domicilio.save(commit=False)
            datos_domicilio.user = socio
            datos_domicilio.save()

            messages.success(request, "Tus datos domiciliarios se han actualizado correctamente.")
            return redirect(reverse('perfil'))
        else:
            # Muestra los errores de validación
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            return render(request, self.template_name, self.get_context_data(form_datos=form_datos, form_domicilio=form_domicilio))