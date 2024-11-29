from ..forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..autenticacion_dni import *
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
import json
from django.urls import reverse
import secrets



stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class signUpPlan(TemplateView):
    template_name = 'app/signUpPlan.html'

class signUpDatos(View):
    template_name = 'app/signUpDatos.html'

    def get(self, request):
        contrato = request.GET.get('contrato')
        print(contrato)

        contrato_info = {
            'Mensual': {
                'duracion': '1 mes',
                'cuota_inscripcion': '15.00€',
                'renovacion': 'tras 1 mes indefinidamente',
                'recision': '14 días antes del fin del contrato',
                'cuota_mensual': '38.99€',
            },
            'Semestral': {
                'duracion': '6 meses',
                'cuota_inscripcion': '15.00€',
                'renovacion': 'tras 6 meses indefinidamente',
                'recision': '14 días antes del fin del contrato',
                'cuota_mensual': '32.99€',
            },
            'Anual': {
                'duracion': '12 meses',
                'cuota_inscripcion': '15.00€',
                'renovacion': 'tras 12 meses indefinidamente',
                'recision': '14 días antes del fin del contrato',
                'cuota_mensual': '24.99€',
            }
        }

        form = FormRegistro()
        detalles_contrato = contrato_info.get(contrato, {})

        context = {
            'contrato': contrato,
            'duracion': detalles_contrato.get('duracion'),
            'cuota_inscripcion': detalles_contrato.get('cuota_inscripcion'),
            'renovacion': detalles_contrato.get('renovacion'),
            'recision': detalles_contrato.get('recision'),
            'cuota_mensual': detalles_contrato.get('cuota_mensual'),
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        contrato = request.GET.get('contrato')  # Recupera el contrato de la URL

        form = FormRegistro(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            request.session['socio_data'] = {
                'nombre': data['socio'].nombre,
                'apellidos': data['socio'].apellidos,
                'fecha_nacimiento': str(data['socio'].fecha_nacimiento),
                'telefono': data['socio'].telefono,
                'email': data['socio'].email,
                'genero': data['socio'].genero,
            }
            request.session['domicilio_data'] = {
                'dni': data['domicilio'].dni,
                'calle': data['domicilio'].calle,
                'ciudad': data['domicilio'].ciudad,
                'codigo_postal': data['domicilio'].codigo_postal,
                'pais': data['domicilio'].pais,
            }

            # Redirige a la próxima vista con el parámetro contrato
            return redirect(f'/InForFit/signUpPago?contrato={contrato}')
        else:
            form = FormRegistro()

        return render(request, self.template_name, {'form': form})


class signUpPago(View):
    template_name = 'app/signUpPago.html'

    def get(self, request):
        # Recuperamos el contrato y mensaje de los parámetros de la URL
        contrato = request.GET.get('contrato')
        mensaje = request.GET.get('mensaje')  # Aquí obtenemos el mensaje de la URL
        print(f'MENSAJE GET: {mensaje}')
        # Obtenemos los datos del socio desde la sesión
        socio_data = request.session.get('socio_data', {})
        nombre = socio_data.get('nombre', '')
        apellidos = socio_data.get('apellidos', '')

        # Información del contrato (duración, cuota, renovación y rescisión)
        contrato_info = {
            'Mensual': {
                'cuota_mensual': 38.99,
                'duracion': '1 mes',
                'cuota_inscripcion': 15.00,
                'renovacion': 'tras 1 mes indefinidamente',
                'recision': '14 días antes del fin del contrato',
            },
            'Semestral': {
                'cuota_mensual': 32.99,
                'duracion': '6 meses',
                'cuota_inscripcion': 15.00,
                'renovacion': 'tras 6 meses indefinidamente',
                'recision': '14 días antes del fin del contrato',
            },
            'Anual': {
                'cuota_mensual': 24.99,
                'duracion': '12 meses',
                'cuota_inscripcion': 15.00,
                'renovacion': 'tras 12 meses indefinidamente',
                'recision': '14 días antes del fin del contrato',
            },
        }

        # Recuperar detalles del contrato basado en la selección
        detalles_contrato = contrato_info.get(contrato, {})
        # Calcular el monto total en centavos
        cuota_mensual = detalles_contrato.get('cuota_mensual', 0.0)
        cuota_inscripcion = detalles_contrato.get('cuota_inscripcion', 0.0)
        monto_total = int((cuota_mensual + cuota_inscripcion) * 100)

        if mensaje in ['success', 'cancel']:
            monto_total = f"{monto_total / 100:.2f}€"
        # Añadimos la información de pago y contrato al contexto
        context = {
            'contrato': contrato,
            'duracion': detalles_contrato.get('duracion'),
            'cuota_inscripcion': f"{cuota_inscripcion:.2f}€",  # Formatear como moneda
            'cuota_mensual': f"{cuota_mensual:.2f}€",  # Formatear como moneda
            'nombre': nombre,
            'apellidos': apellidos,
            'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,  # Clave pública de Stripe
            'monto_total': monto_total,
            'renovacion': detalles_contrato.get('renovacion'),  # Nueva clave para renovacion
            'recision': detalles_contrato.get('recision'),  # Nueva clave para recision
            'mensaje': mensaje  # Aquí agregamos el mensaje al contexto
        }

        return render(request, self.template_name, context)

    def post(self, request):
        try:
            # Parsear datos de la solicitud JSON
            data = json.loads(request.body)
            monto_total = data.get('monto_total', 0)
            contrato = data.get('contrato', 'Mensual')

            # Obtener información del socio de la sesión
            socio_data = request.session.get('socio_data', {})
            nombre = socio_data.get('nombre', '')
            apellidos = socio_data.get('apellidos', '')
            print(f'SOCIO_DTA POST: {socio_data}')

            # Detalles del contrato
            contrato_info = {
                'Mensual': {
                    'cuota_mensual': 38.99,
                    'duracion': '1 mes',
                    'cuota_inscripcion': 15.00,
                    'renovacion': 'tras 1 mes indefinidamente',
                    'recision': '14 días antes del fin del contrato',
                },
                'Semestral': {
                    'cuota_mensual': 32.99,
                    'duracion': '6 meses',
                    'cuota_inscripcion': 15.00,
                    'renovacion': 'tras 6 meses indefinidamente',
                    'recision': '14 días antes del fin del contrato',
                },
                'Anual': {
                    'cuota_mensual': 24.99,
                    'duracion': '12 meses',
                    'cuota_inscripcion': 15.00,
                    'renovacion': 'tras 12 meses indefinidamente',
                    'recision': '14 días antes del fin del contrato',
                },
            }
            detalles_contrato = contrato_info.get(contrato, {})
            cuota_mensual = detalles_contrato.get('cuota_mensual', 0.0)
            cuota_inscripcion = detalles_contrato.get('cuota_inscripcion', 0.0)
            print(cuota_mensual)
            print(cuota_inscripcion)
            return_url = f"{request.build_absolute_uri(reverse('signupPago'))}?contrato={contrato}&mensaje=success&cuota_mensual={cuota_mensual}&cuota_inscripcion={cuota_inscripcion}"
            print(return_url)

            intent = stripe.PaymentIntent.create(
                amount=monto_total,
                currency='eur',
                payment_method=data['payment_method_id'],
                confirmation_method='manual',
                confirm=True,
                return_url=return_url
            )

            if intent.status == 'succeeded':
                # Si el pago fue exitoso, guardar en la base de datos
                print('SUCCEDED')
                # Recuperamos los datos del socio desde la sesión
                domicilio_data = request.session.get('domicilio_data', {})
# Recuperamos los datos de domicilio desde la sesión
                email=domicilio_data['email']
                dni=domicilio_data['dni']
                print(f'SOCIO DATA: {socio_data}')
                print(f'DOMICILIO DATA: {domicilio_data}')

                try:
                    usuario_existente = User.objects.filter(username=dni).exists() or User.objects.filter(
                        email=email).exists()

                    if usuario_existente:
                        return JsonResponse({'usuario_existente': True})

                    # Si no existe, crear uno nuevo
                    password = secrets.token_urlsafe(8)  # Contraseña aleatoria segura
                    nuevo_usuario = User.objects.create_user(
                        username=dni,
                        email=email,
                        password=password,
                        first_name=socio_data['nombre'],
                        last_name=socio_data['apellidos'],
                    )

                    # Crear instancia de Socio
                    socio_obj = Socio.objects.create(
                        user=nuevo_usuario,
                        nombre=socio_data['nombre'],
                        apellidos=socio_data['apellidos'],
                        fecha_nacimiento=socio_data['fecha_nacimiento'],
                        telefono=socio_data['telefono'],
                        email=email,
                        genero=socio_data['genero'],
                    )

                    # Crear instancia de DatosDomicilio
                    DatosDomicilio.objects.create(
                        user=socio_obj,
                        dni=dni,
                        calle=domicilio_data['calle'],
                        ciudad=domicilio_data['ciudad'],
                        codigo_postal=domicilio_data['codigo_postal'],
                        pais=domicilio_data['pais'],
                    )

                    # Proceso de suscripción
                    duraciones = {'Mensual': 30, 'Semestral': 180, 'Anual': 365}
                    duracion_contrato = duraciones.get(contrato, 30)
                    fecha_inicio = timezone.now().date()
                    fecha_vencimiento = fecha_inicio + timezone.timedelta(days=duracion_contrato)

                    Suscripción.objects.create(
                        user=socio_obj,
                        nombre=contrato,
                        precio_suscripcion=data['cuota_mensual'],
                        precio_inscripcion=data['cuota_inscripcion'],
                        duracion=duracion_contrato,
                        fecha_inicio=fecha_inicio,
                        fecha_vencimiento=fecha_vencimiento,
                    )

                    return JsonResponse({'usuario_existente': False, 'status': 'success'})

                except Exception as e:
                    print(f"Error al procesar los datos: {e}")
                    return JsonResponse({'status': 'error', 'message': 'Error al procesar los datos'})

        except stripe.error.CardError as e:
            return JsonResponse({'status': 'cancel', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'cancel', 'message': 'Hubo un error procesando el pago'})

class logIn(View):
    form_class = FormLogIn
    initial = {"key": "value"}
    template_name = "app/logIn.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Obtener DNI y contraseña del formulario
            dni = form.cleaned_data.get('dni')
            password = form.cleaned_data.get('password')
            print(dni)
            print(password)

            # Autenticar usando el DNI
            user = authenticate(username=dni, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'welcome')  # Si 'next' no está presente, redirige a 'index'
                return redirect(next_url)
            else:
                form.add_error(None, "Credenciales inválidas. Por favor, intente de nuevo.")

        return render(request, self.template_name, {"form": form})


class logOut(View):
    def get(self, request):
        logout(request)
        return redirect('welcome')

