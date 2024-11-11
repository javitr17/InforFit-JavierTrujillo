from ..forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..autenticacion_dni import *

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

        # Crear una instancia del formulario unificado
        form = FormRegistro()

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
            'form': form,  # El formulario unificado se pasa al contexto
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = FormRegistro(request.POST)
        if form.is_valid():
            # Guardar los datos de socio y domicilio
            form.save()
            return redirect('some-success-page')  # Redirigir a una página de éxito
        return render(request, self.template_name, {'form': form})

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

