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

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class signUpPlan(TemplateView):
    template_name = 'app/signUpPlan.html'


class signUpDatos(View):
    template_name = 'app/signUpDatos.html'


    def get(self, request):
        # Obtener el parámetro 'contrato' de la URL
        contrato = request.GET.get('contrato')
        print(contrato)
        # Definir los detalles de cada tipo de contrato
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
        formSocio = FormDatosSocio()
        formDomicilio=FormDatosDomicilio()
        # Recuperar los detalles según el contrato seleccionado
        detalles_contrato = contrato_info.get(contrato, {})

        # Pasar los detalles al contexto del template
        context = {
            'contrato': contrato,
            'duracion': detalles_contrato.get('duracion'),
            'cuota_inscripcion': detalles_contrato.get('cuota_inscripcion'),
            'renovacion': detalles_contrato.get('renovacion'),
            'recision': detalles_contrato.get('recision'),
            'cuota_mensual': detalles_contrato.get('cuota_mensual'),
            'form_socio': formSocio,
            'form_domicilio': formDomicilio,
        }
        return render(request, self.template_name, context)

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
        contrato = request.GET.get('contrato')
        socio_data = request.session.get('socio_data', {})
        nombre = socio_data.get('nombre', '')
        apellidos = socio_data.get('apellidos', '')

        contrato_info = {
            'Mensual': {'cuota_mensual': 38.99, 'duracion': '1 mes', 'cuota_inscripcion': 15.00},
            'Semestral': {'cuota_mensual': 32.99, 'duracion': '6 meses', 'cuota_inscripcion': 15.00},
            'Anual': {'cuota_mensual': 24.99, 'duracion': '12 meses', 'cuota_inscripcion': 15.00},
        }

        # Extraer los detalles del contrato
        detalles_contrato = contrato_info.get(contrato, {})
        if not detalles_contrato:
            # Si no hay detalles para el contrato, redirigir al formulario de selección
            return redirect('signupPlan')

        # Calcular el monto total en centavos
        cuota_mensual = detalles_contrato.get('cuota_mensual', 0.0)
        cuota_inscripcion = detalles_contrato.get('cuota_inscripcion', 0.0)
        monto_total = int((cuota_mensual + cuota_inscripcion) * 100)

        context = {
            'contrato': contrato,
            'duracion': detalles_contrato.get('duracion'),
            'cuota_inscripcion': f"{cuota_inscripcion:.2f}€",  # Formatear como moneda
            'cuota_mensual': f"{cuota_mensual:.2f}€",  # Formatear como moneda
            'nombre': nombre,
            'apellidos': apellidos,
            'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
            'monto_total': monto_total,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        # Recuperar los datos del formulario
        contrato = request.POST.get('contrato')
        socio_data = request.session.get('socio_data', {})
        detalles_contrato = {
            'Mensual': {'cuota_mensual': 38.99, 'cuota_inscripcion': 15.00},
            'Semestral': {'cuota_mensual': 32.99, 'cuota_inscripcion': 15.00},
            'Anual': {'cuota_mensual': 24.99, 'cuota_inscripcion': 15.00},
        }.get(contrato, {})

        if not detalles_contrato:
            return redirect('signupPlan')

        cuota_mensual = detalles_contrato['cuota_mensual']
        cuota_inscripcion = detalles_contrato['cuota_inscripcion']
        monto_total = int((cuota_mensual + cuota_inscripcion) * 100)

        # Recuperar el token Stripe que viene desde el frontend
        token = request.POST.get('stripeToken')

        if not token:
            return JsonResponse({'status': 'error', 'message': 'Token no proporcionado'})

        try:
            # Crear la sesión de pago en Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {'name': f"Plan {contrato}"},
                            'unit_amount': int(cuota_mensual * 100),  # Convertir a centavos
                        },
                        'quantity': 1,
                    },
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {'name': 'Cuota de inscripción'},
                            'unit_amount': int(cuota_inscripcion * 100),  # Convertir a centavos
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(''),
                cancel_url=request.build_absolute_uri('/signUpPlan'),
            )

            # Redirigir a Stripe Checkout
            return redirect(session.url)

        except stripe.error.CardError as e:
            # Manejo de errores de Stripe (tarjeta rechazada, etc.)
            return render(request, self.template_name, {
                'error': f"Error al procesar el pago: {e.user_message}"
            })
        except Exception as e:
            # Manejo de otros posibles errores
            return render(request, self.template_name, {
                'error': f"Error desconocido: {str(e)}"
            })


# views.py


class cancel(TemplateView):
    template_name = 'app/cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'El pago fue cancelado. Si tienes alguna duda, por favor contacta con nosotros.'
        return context


class charge(TemplateView):
    template_name = 'app/charge.html'

    def get_context_data(self, **kwargs):
        # Aquí puedes agregar más información relevante sobre el pago si es necesario
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session_id')
        context['message'] = 'Tu pago fue completado con éxito.'
        context['session_id'] = session_id  # O cualquier otra información relacionada con la sesión
        return context
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

