from app.forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

class signUp(View):
    template_name = 'app/signUp.html'
    form_class = FormSignUp

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('index')
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
        return_render = render(request, self.template_name, {"form": form})
        if form.is_valid():
            # <process form cleaned data>
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            next_ruta = request.GET.get('next')
            user = authenticate(username=username, password=password)
            print("Contenido de la sesión antes de iniciar sesión:",
                  request.session)  # Agregar este mensaje para depurar
            print(user)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'index')  # Si 'next' no está presente, redirige a 'chat'
                return redirect(next_url)
                print('Credenciales inválidas. Por favor, intente de nuevo.')
                return render(request, self.template_name, {"form": form})


class logOut(View):
    def get(self, request):
        logout(request)
        return redirect('index')
