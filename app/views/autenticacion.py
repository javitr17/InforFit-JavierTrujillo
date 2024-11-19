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

        # Recuperar datos de la sesión
        socio_data = request.session.get('socio_data', {})
        nombre = socio_data.get('nombre', '')
        apellidos = socio_data.get('apellidos', '')

        # Recuperar los detalles según el contrato seleccionado
        detalles_contrato = contrato_info.get(contrato, {})

        # Pasar los datos al contexto del template
        context = {
            'contrato': contrato,
            'duracion': detalles_contrato.get('duracion'),
            'cuota_inscripcion': detalles_contrato.get('cuota_inscripcion'),
            'renovacion': detalles_contrato.get('renovacion'),
            'recision': detalles_contrato.get('recision'),
            'cuota_mensual': detalles_contrato.get('cuota_mensual'),
            'nombre': nombre,  # Agregar el nombre al contexto
            'apellidos': apellidos,  # Agregar los apellidos al contexto
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = FormRegistro(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            # Almacena los objetos en la sesión para su uso posterior
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

            # Redirige a la próxima vista
            return redirect('signupPago')
        else:
            form = FormRegistro()

        return render(request, 'template_form.html', {'form': form})

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

