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
from celery import shared_task
from django.conf import settings
import json
from django.urls import reverse
import secrets
from datetime import timedelta
from django.contrib.auth.mixins import AccessMixin
from decimal import Decimal, ROUND_HALF_UP



stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@shared_task
def procesar_pagos_diarios():
    today = timezone.now().date()

    # Obtener todos los socios con suscripciones activas
    socios_con_suscripciones_activas = Suscripción.objects.filter(suscripcion_activa=True)

    for suscripcion in socios_con_suscripciones_activas:
        socio = suscripcion.user
        tarjeta = TarjetaPago.objects.filter(user=socio).first()

        if tarjeta:
            # Verificar si la fecha de proximo_pago coincide con la fecha actual
            if suscripcion.proximo_pago.date() == today:
                # Procesar el pago con Stripe para la cuota de suscripción
                monto_total = int(suscripcion.precio_suscripcion * 100)  # Convertir a centavos

                # Intentar realizar el pago
                try:
                    # Crear un PaymentIntent
                    intent = stripe.PaymentIntent.create(
                        amount=monto_total,
                        currency='eur',
                        payment_method=tarjeta.token_stripe,
                        confirmation_method='manual',
                        confirm=True
                    )

                    if intent.status == 'succeeded':
                        # Si el pago es exitoso, actualizar los datos de la suscripción
                        if suscripcion.nombre == 'Mensual':
                            duracion = timedelta(days=30)
                        elif suscripcion.nombre == 'Semestral':
                            duracion = timedelta(days=180)
                        elif suscripcion.nombre == 'Anual':
                            duracion = timedelta(days=365)
                        else:
                            duracion = timedelta(days=30)  # Valor predeterminado

                        fecha_inicio = timezone.now()
                        fecha_vencimiento = fecha_inicio + duracion

                        # Actualizar suscripción con nuevas fechas
                        suscripcion.fecha_inicio = fecha_inicio
                        suscripcion.fecha_vencimiento = fecha_vencimiento
                        suscripcion.proximo_pago = fecha_vencimiento

                        suscripcion.save()
                        print(f"[INFO] Pago procesado y suscripción de {socio} actualizada.")
                    else:
                        print(f"[ERROR] El pago de {socio} no fue exitoso.")

                except stripe.error.StripeError as e:
                    print(f"[ERROR] StripeError al procesar el pago para {socio}: {str(e)}")
        else:
            print(f"[ERROR] No se encontró tarjeta de pago registrada para {socio}.")

class SoloNoAutenticadosMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # Verificamos si el parámetro `allow_access` está presente en la URL
        allow_access = request.GET.get('allow_access')

        # Si el usuario está autenticado y el parámetro `allow_access` no está presente, redirigimos
        if request.user.is_authenticated and not allow_access:
            return redirect('welcome')  # Redirige al usuario autenticado a la página de bienvenida

        # Si no está autenticado o el parámetro `allow_access` está presente, continuamos con el flujo normal
        return super().dispatch(request, *args, **kwargs)

class signUpPlan(SoloNoAutenticadosMixin, TemplateView):
    template_name = 'app/signUpPlan.html'

class signUpDatos(SoloNoAutenticadosMixin, View):
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

            password = form.cleaned_data.get('password')  # Aquí obtenemos la contraseña
            request.session['password'] = password

            # Redirige a la próxima vista con el parámetro contrato
            return redirect(f'/InForFit/signUpPago?contrato={contrato}')

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


class signUpPago(SoloNoAutenticadosMixin, View):
    template_name = 'app/signUpPago.html'

    def get(self, request):
        # Recuperamos el contrato y mensaje de los parámetros de la URL
        contrato = request.GET.get('contrato')
        mensaje = request.GET.get('mensaje')  # Obtenemos el mensaje de la URL
        print(f'MENSAJE GET: {mensaje}')

        # Obtenemos los datos del socio desde la sesión
        socio_data = request.session.get('socio_data', {})
        print(f"Socio data en GET: {socio_data}")
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

        detalles_contrato = contrato_info.get(contrato, {})

        # Calcular el monto total en centavos (convertir a Decimal antes de operar)
        cuota_mensual = detalles_contrato.get('cuota_mensual', 0.0)
        cuota_inscripcion = detalles_contrato.get('cuota_inscripcion', 0.0)

        # Convertir los valores a Decimal (evitar problemas de precisión con floats)
        cuota_mensual = Decimal(str(cuota_mensual))  # Asegurarse de convertir como string
        cuota_inscripcion = Decimal(str(cuota_inscripcion))  # Asegurarse de convertir como string

        # Imprimir los valores de las cuotas para verificación
        print(f'CUOTA MENSUAL: {cuota_mensual}')
        print(f'CUOTA INSCRIPCION: {cuota_inscripcion}')

        # Calcular el monto total
        monto_total = cuota_mensual + cuota_inscripcion

        # Redondear el monto total a 2 decimales (en formato de centavos)
        monto_total = monto_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Mostrar el monto total en euros, sin necesidad de dividir entre 100
        total_pagar = f"{monto_total:.2f}€"  # No dividimos por 100 aquí

        # Formatear el mensaje si ya existe uno (por ejemplo, "success" o "cancel")
        if mensaje in ['success', 'cancel']:
            total_pagar = f"{monto_total:.2f}€"

        # Mostrar el monto total
        print(f'MONTO TOTAL: {total_pagar}')

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
            'mensaje': mensaje,  # Aquí agregamos el mensaje al contexto
            'total_pagar': total_pagar
        }

        return render(request, self.template_name, context)

    def post(self, request):
        try:
            socio_data = request.session.get('socio_data', {})
            domicilio_data = request.session.get('domicilio_data', {})
            password = request.session.get('password')
            print(f"[DEBUG] Socio Data POST: {socio_data}")
            print(f"[DEBUG] Domicilio Data POST: {domicilio_data}")

            data = json.loads(request.body)
            print(f"[DEBUG] Datos del cliente: {data}")

            monto_total = data.get('monto_total')
            monto_total = int(Decimal(str(monto_total)) * 100)
            contrato = data.get('contrato')
            print(f'CONTRATO: {contrato}')
            if contrato== 'Anual':
                precio_suscripcion =24.99
                precio_inscripcion =15.00
                duracion ='12 meses'
                fecha_inicio =timezone.now()
                fecha_vencimiento =fecha_inicio + timedelta(days=365)
                proximo_pago=fecha_inicio + timedelta(days=30)
            elif contrato == 'Semestral':
                precio_suscripcion = 32.99
                precio_inscripcion = 15.00
                duracion = '6 meses'
                fecha_inicio = timezone.now()
                fecha_vencimiento = fecha_inicio + timedelta(days=180)
                proximo_pago = fecha_inicio + timedelta(days=30)
            elif contrato == 'Mensual':
                precio_suscripcion = 38.99
                precio_inscripcion = 15.00
                duracion = '1 mes'
                fecha_inicio = timezone.now()
                fecha_vencimiento = fecha_inicio + timedelta(days=30)
                proximo_pago = fecha_inicio + timedelta(days=30)

            print(f'fecha_inicio: {fecha_inicio}')
            print(f'fecha_vencimiento: {fecha_vencimiento}')
            print(f'proximo_pago: {proximo_pago}')

            email = socio_data.get('email')
            dni = domicilio_data.get('dni')
            if User.objects.filter(username=dni).exists() or User.objects.filter(email=email).exists():
                print(f"[WARNING] Usuario con DNI: {dni} o email: {email} ya existe.")
                return JsonResponse({'usuario_existente': True})

            payment_method_id = data.get('payment_method_id')
            card_holder_name = data.get('card_holder_name')

            if not all([monto_total, contrato, payment_method_id, card_holder_name]):
                print("[ERROR] Faltan datos requeridos para procesar el pago.")
                return JsonResponse({'status': 'cancel', 'message': 'Faltan datos requeridos.'})

            return_url = f"{request.build_absolute_uri(reverse('signupPago'))}?contrato={contrato}"
            print(f"[DEBUG] URL de retorno: {return_url}")

            intent = stripe.PaymentIntent.create(
                amount=monto_total,
                currency='eur',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url=return_url
            )
            print(f"[DEBUG] Stripe PaymentIntent creado: {intent}")

            if intent.status == 'succeeded':
                print("[INFO] Pago completado exitosamente.")

                charge_id = intent.get('latest_charge')
                if not charge_id:
                    print("[ERROR] No se encontró un cargo asociado al intento de pago.")
                    return JsonResponse({'status': 'cancel', 'message': 'Error al procesar el pago.'})

                charge = stripe.Charge.retrieve(charge_id)
                print(f"[DEBUG] Detalles del cargo: {charge}")

                email = socio_data.get('email')
                dni = domicilio_data.get('dni')
                if User.objects.filter(username=dni).exists() or User.objects.filter(email=email).exists():
                    print(f"[WARNING] Usuario con DNI: {dni} o email: {email} ya existe.")
                    return JsonResponse({'usuario_existente': True})

                # Envolver en una transacción atómica
                with transaction.atomic():
                    # Crear usuario y datos relacionados

                    nuevo_usuario = User.objects.create_user(
                        username=dni,
                        email=email,
                        password=password,
                        first_name=socio_data['nombre'],
                        last_name=socio_data['apellidos'],
                    )
                    socio_obj = Socio.objects.create(
                        user=nuevo_usuario,
                        nombre=socio_data['nombre'],
                        apellidos=socio_data['apellidos'],
                        fecha_nacimiento=socio_data['fecha_nacimiento'],
                        telefono=socio_data['telefono'],
                        email=email,
                        genero=socio_data['genero'],
                    )

                    Suscripción.objects.create(
                        user=socio_obj,
                        nombre=contrato,
                        precio_suscripcion= precio_suscripcion,
                        precio_inscripcion=precio_inscripcion,
                        duracion=duracion,
                        fecha_inicio= fecha_inicio,
                        fecha_vencimiento= fecha_vencimiento,
                        proximo_pago= proximo_pago,
                    )

                    DatosDomicilio.objects.create(
                        user=socio_obj,
                        dni=dni,
                        calle=domicilio_data['calle'],
                        ciudad=domicilio_data['ciudad'],
                        codigo_postal=domicilio_data['codigo_postal'],
                        pais=domicilio_data['pais'],
                    )
                    # Crear tarjeta de pago
                    TarjetaPago.objects.create(
                        user=socio_obj,
                        token_stripe=payment_method_id,
                        ult_cuatro_digitos=charge.payment_method_details.card.last4,
                        fecha_ven_parcial=f"{charge.payment_method_details.card.exp_month}/{str(charge.payment_method_details.card.exp_year)[-2:]}",
                        nombre_titular=card_holder_name,
                    )
                    print("[INFO] Tarjeta de pago registrada.")
                    login(request, nuevo_usuario)
                    print("[INFO] Usuario autenticado automáticamente.")

                return JsonResponse({'usuario_existente': False, 'status': 'success'})

            else:
                print(f"[WARNING] Intento de pago fallido: {intent.status}")
                return JsonResponse({'status': 'cancel', 'message': 'Error en el intento de pago.'})

        except stripe.error.CardError as e:
            print(f"[ERROR] Stripe CardError: {str(e)}")
            return JsonResponse({'status': 'cancel', 'message': str(e)})

        except stripe.error.StripeError as e:
            print(f"[ERROR] StripeError: {str(e)}")
            return JsonResponse({'status': 'cancel', 'message': 'Error en el servicio de pago.'})

        except Exception as e:
            print(f"[ERROR] Excepción no manejada: {str(e)}")
            return JsonResponse({'status': 'cancel', 'message': 'Error inesperado al procesar el pago.'})

class logIn(SoloNoAutenticadosMixin, View):
    form_class = FormLogIn
    initial = {"key": "value"}
    template_name = "app/logIn.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        print(request.POST)  # Depura qué datos se están enviando en el formulario

        form = self.form_class(request.POST)
        error_messages = []  # Lista para errores de lógica del negocio

        if form.is_valid():
            # Obtener DNI y contraseña
            dni = form.cleaned_data.get('dni')
            password = form.cleaned_data.get('password')
            print(f'USUARIO {dni}')
            print(f'CONTRASEÑA {password}')
            # Autenticar al usuario
            user = authenticate(username=dni, password=password)

            if user is not None:
                print('usuario valido')
                # Si el usuario es superusuario, saltamos verificación de suscripción
                if user.is_superuser:
                    login(request, user)
                    next_url = request.GET.get('next', 'welcome')
                    return redirect(next_url)

                # Verificación de la suscripción para usuarios normales
                try:
                    socio = Socio.objects.get(user=user)
                    suscripcion = Suscripción.objects.filter(user=socio).first()

                    if not suscripcion:
                        error_messages.append("No se encontró una suscripción para este socio.")
                    elif not suscripcion.suscripcion_activa:
                        error_messages.append("El socio no está actualmente suscrito a ningún plan.")
                except Socio.DoesNotExist:
                    error_messages.append("No se encontró el socio asociado al usuario.")

                # Si hay errores de suscripción, mostramos los mensajes
                if error_messages:
                    return render(request, self.template_name, {"form": form, "error_messages": error_messages})

                # Si todo está correcto, iniciamos sesión
                login(request, user)
                next_url = request.GET.get('next', 'welcome')
                return redirect(next_url)
            else:
                error_messages.append("Credenciales inválidas. Por favor, intente de nuevo.")
        else:
            # Errores de validación del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{error}")

        # Renderizamos la plantilla con los errores
        return render(request, self.template_name, {"form": form, "error_messages": error_messages})

class logOut(View):
    def get(self, request):
        logout(request)
        return redirect('welcome')

