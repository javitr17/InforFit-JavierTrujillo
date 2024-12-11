from django.urls import path
from .views.autenticacion import *
from .views.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('signUpPlan', signUpPlan.as_view(), name='signupPlan'),
    path('signUpDatos', signUpDatos.as_view(), name='signupDatos'),
    path('signUpPago', signUpPago.as_view(), name='signupPago'),
    path('perfil', perfil.as_view(), name='perfil'),
    path('logIn', logIn.as_view(), name='login'),
    path('logOut', logOut.as_view(), name='logout'),

]