from ..forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..autenticacion_dni import *

class signUpPlan(View):
    template_name = 'app/signUpPlan.html'
    form_class = FormSignUp

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            dni = form.cleaned_data['dni']
            password = form.cleaned_data['password']
            print(dni)
            print(password)
            user = User(username=dni)
            user.set_password(password)
            user.save()

            login(request, user)
            return redirect('welcome')
        return render(request, self.template_name, {'form': form})

class signUpDatos(View):
    template_name = 'app/signUpDatos.html'
    form_class = FormSignUp

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            dni = form.cleaned_data['dni']
            password = form.cleaned_data['password']
            print(dni)
            print(password)
            user = User(username=dni)
            user.set_password(password)
            user.save()

            login(request, user)
            return redirect('welcome')
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

