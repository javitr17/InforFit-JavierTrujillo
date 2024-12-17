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
from datetime import timedelta
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from ..preguntarIA import *
from datetime import datetime
from django.views.generic.edit import FormView



@method_decorator(login_required(login_url='login'), name='dispatch')
class perfil(TemplateView):
    template_name = 'app/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        socio = Socio.objects.filter(user=self.request.user).first()

        if socio:
            form_datos = FormDatosSocio(instance=socio)
            domicilio = socio.datosdomicilio_set.first()
            form_cambio_contraseña = FormCambioContraseña(user=self.request.user)

            if domicilio:
                form_domicilio = FormDatosDomicilio(instance=domicilio)
            else:
                form_domicilio = FormDatosDomicilio()

            context.update({
                'form_datos': form_datos,
                'form_domicilio': form_domicilio,
                'form_cambio_contraseña': form_cambio_contraseña,
                'nombre': socio.nombre.upper(),
                'apellidos': socio.apellidos.upper(),
                'id': socio.id,
            })

            suscripcion = Suscripción.objects.filter(user=socio).first()
            precios = {'Anual': 24.99, 'Semestral': 32.99, 'Mensual': 38.99}
            duraciones={'Anual': '12 meses', 'Semestral': '6 meses', 'Mensual': '1 mes'}
            if suscripcion:
                planes_disponibles = ['Anual', 'Semestral', 'Mensual']
                planes_disponibles.remove(suscripcion.nombre)

                context.update({
                    'contrato': suscripcion.nombre,
                    'precio_suscripcion': precios[suscripcion.nombre],
                    'fecha_inicio': suscripcion.fecha_inicio.strftime('%d/%m/%Y'),
                    'fecha_vencimiento': suscripcion.fecha_vencimiento.strftime('%d/%m/%Y'),
                    'proximo_pago': suscripcion.proximo_pago.strftime('%d/%m/%Y'),
                    'otros_planes': planes_disponibles,
                    'precios': precios,
                    'duraciones':duraciones,
                    'fecha_vigencia': suscripcion.proximo_pago.strftime('%d/%m/%Y'),
                })
            else:
                context.update({
                    'contrato': None,
                    'precio_suscripcion': None,
                    'fecha_inicio': None,
                    'fecha_vencimiento': None,
                    'proximo_pago': None,
                    'otros_planes': [],
                    'precios': precios,
                    'duraciones': duraciones,
                    'fecha_vigencia': None,
                })
        else:
            messages.error(self.request, "No se encontró un socio asociado al usuario.")
            return redirect('perfil')

        return context


    def post(self, request, *args, **kwargs):
        socio = Socio.objects.filter(user=request.user).first()
        if not socio:
            messages.error(request, "No se encontró un socio asociado al usuario.")
            return redirect('perfil')

        form_datos = FormDatosSocio(request.POST, instance=socio)


        if form_datos.is_valid():
            print('FORM DATOS VALIDO')
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
        else:
            print('FORM DATOS NO VALIDO')
            print(form_datos.errors)  # Esto imprime los errores del formulario

        # Si se actualizan los datos domiciliarios
        domicilio = socio.datosdomicilio_set.first()
        form_domicilio = FormDatosDomicilio(request.POST, instance=domicilio)

        # Validar y guardar los datos de domicilio
        if form_domicilio.is_valid():
            form_domicilio.save()
            messages.success(request, "Tus datos domiciliarios se han actualizado correctamente.")
            return redirect(reverse('perfil'))

        form_cambio_contraseña = FormCambioContraseña(user=request.user, data=request.POST)
        if form_cambio_contraseña.is_valid():
            form_cambio_contraseña.save()
            messages.success(request, "Tu contraseña se ha actualizado correctamente.")
            return redirect(reverse('perfil'))
        nuevo_plan = request.POST.get('nuevo_plan')

        if nuevo_plan:
            precios = {'Anual': 24.99, 'Semestral': 32.99, 'Mensual': 38.99}
            duraciones = {'Anual': 365, 'Semestral': 180, 'Mensual': 30}
            suscripcion = Suscripción.objects.filter(user=socio).first()

            if suscripcion:
                suscripcion.nombre = nuevo_plan
                suscripcion.precio = precios[nuevo_plan]
                suscripcion.fecha_inicio = suscripcion.proximo_pago
                suscripcion.fecha_vencimiento = suscripcion.proximo_pago + timedelta(days=duraciones[nuevo_plan])
                suscripcion.proximo_pago = suscripcion.proximo_pago
                suscripcion.save()

                messages.success(request, "Tu plan de suscripción ha sido actualizado correctamente.")
                return redirect(reverse('perfil'))

        if 'darme_baja' in request.POST:  # Detectamos la solicitud de baja
            suscripcion = Suscripción.objects.filter(user=socio).first()
            if suscripcion:
                print('BAJA CONFIRMADA')
                suscripcion.suscripcion_activa = False  # Desactivamos la suscripción
                suscripcion.save()

                messages.success(request, "Tu suscripción ha sido cancelada.")
                return redirect(reverse('perfil'))

        if 'imagen' in request.FILES:
            socio.imagen = request.FILES['imagen']
            socio.save()
            request.session['mostrar_animacion'] = True

            # Devuelve una respuesta JSON en lugar de redirigir
            return JsonResponse({"success": True})

        else:
            # Muestra los errores de validación
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            return render(request, self.template_name, self.get_context_data(form_datos=form_datos, form_domicilio=form_domicilio))

@method_decorator(login_required(login_url='login'), name='dispatch')
class entrenamiento(TemplateView):
    template_name = 'app/entrenamiento.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class rutina(TemplateView):
    template_name = 'app/rutina.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Recuperar el parámetro de la URL y convertirlo a mayúsculas
        sitio = self.kwargs.get('sitio', None)  # 'parametro' es el nombre del parámetro en la URL
        print(f'SITIO: '+sitio)
        if sitio:
            sitio = sitio.upper()  # Convertir a mayúsculas

        # Agregar el parámetro y el formulario al contexto
        form = FormEntrenamiento()
        context['form'] = form
        context['sitio'] = sitio  # Pasar el parámetro al contexto

        return context

    def post(self, request, *args, **kwargs):
        form = FormEntrenamiento(request.POST)
        sitio = self.kwargs.get('sitio', None)
        if form.is_valid():
            # Procesar datos del formulario
            dias_a_la_semana = form.cleaned_data['dias_a_la_semana']
            tiempo_del_entreno = form.cleaned_data['tiempo_del_entreno']
            nivel_de_la_persona = form.cleaned_data['nivel_de_la_persona']
            objetivo = form.cleaned_data['objetivo']

            respuesta = preguntarIA(sitio, dias_a_la_semana, tiempo_del_entreno, nivel_de_la_persona, objetivo)

            # Crear la respuesta HTTP para el PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="rutina_personalizada.pdf"'

            # Crear el documento PDF
            p = canvas.Canvas(response, pagesize=letter)

            # Establecer la fuente para el texto
            p.setFont('Helvetica', 12)
            p.setFillColor(colors.black)  # Color negro para el texto

            # El texto a añadir al PDF

            # Crear un objeto de texto para que se ajuste automáticamente
            text_object = p.beginText(40, 750)  # Posición inicial
            text_object.setFont('Helvetica', 12)
            text_object.setTextOrigin(40, 750)
            text_object.textLines(respuesta)

            # Dibujar el texto en el PDF
            p.drawText(text_object)

            # Mostrar la página
            p.showPage()
            p.save()

            return response

        return render(request, self.template_name, {'form': form})

@method_decorator(login_required(login_url='login'), name='dispatch')
class progreso(TemplateView):
    template_name = 'app/progreso.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el socio asociado al usuario actual
        if self.request.user.is_authenticated:
            socio = get_object_or_404(Socio, user=self.request.user)

            # Obtener los datos físicos más recientes del socio
            datos_fisicos = DatosFisicos.objects.filter(user=socio).last()

            if datos_fisicos:
                # Truncar el peso a los dos primeros dígitos
                if datos_fisicos.peso:
                    peso_str = str(datos_fisicos.peso)  # Convertir a cadena
                    peso_actual = float(peso_str[:2])  # Convertir los dos primeros dígitos a float
                else:
                    peso_actual = None

                # Obtener la altura
                altura_actual = datos_fisicos.altura

                # Calcular el IMC si ambos valores están disponibles
                if peso_actual and altura_actual:
                    altura_metros = float(altura_actual) / 100  # Convertir a metros
                    imc = round(peso_actual / (altura_metros ** 2), 2)  # Cálculo del IMC
                else:
                    imc = None
            else:
                peso_actual = None
                altura_actual = None
                imc = None

            # Pasar los valores al contexto
            context['peso_actual'] = peso_actual
            context['altura_actual'] = altura_actual
            context['imc'] = imc

        return context
@method_decorator(login_required(login_url='login'), name='dispatch')
class PesoDataView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Usuario no autenticado'}, status=403)

        # Obtener el socio del usuario autenticado
        socio = get_object_or_404(Socio, user=request.user)
        datos = DatosFisicos.objects.filter(user=socio)

        # Preparar los datos en el formato que FullCalendar espera
        data = [
            {
                'title': f'Peso: {dato.peso} kg',  # El título con el peso
                'start': dato.fecha.strftime('%Y-%m-%dT%H:%M:%S'),  # Fecha en formato ISO
                'end': dato.fecha.strftime('%Y-%m-%dT%H:%M:%S'),  # Puede ser la misma fecha o puedes agregar tiempo
            }
            for dato in datos
        ]
        return JsonResponse(data, safe=False)

@method_decorator(login_required(login_url='login'), name='dispatch')
class datosFisicos(TemplateView):
    template_name = 'app/datosFisicos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el socio asociado al usuario
        if self.request.user.is_authenticated:
            socio = get_object_or_404(Socio, user=self.request.user)

            # Obtener los datos físicos más recientes del socio
            datos_fisicos = DatosFisicos.objects.filter(user=socio).last()

            # Inicializar los formularios con los datos existentes
            if datos_fisicos:
                context['peso_form'] = FormPeso(initial={'peso': datos_fisicos.peso})
                context['altura_form'] = FormAltura(initial={'altura': datos_fisicos.altura})
            else:
                context['peso_form'] = FormPeso()
                context['altura_form'] = FormAltura()

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Usuario no autenticado'}, status=403)

        socio = get_object_or_404(Socio, user=request.user)

        # Procesar el formulario de peso
        if 'peso' in request.POST:
            form = FormPeso(request.POST)
            if form.is_valid():
                peso = form.cleaned_data['peso']
                # Actualizar o crear los datos de peso
                DatosFisicos.objects.create(
                    user=socio,
                    peso=peso,
                    fecha=now()  # Fecha actual
                )
                return JsonResponse({'status': 'success', 'message': 'Peso registrado'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        # Procesar el formulario de altura
        elif 'altura' in request.POST:
            form = FormAltura(request.POST)
            if form.is_valid():
                altura = form.cleaned_data['altura']
                print(altura)
                # Actualizar o crear los datos de altura
                DatosFisicos.objects.create(
                    user=socio,
                    altura=altura,
                    fecha=now()  # Fecha actual
                )
                return JsonResponse({'status': 'success', 'message': 'Altura registrada'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Formulario no reconocido'}, status=400)