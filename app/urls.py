from django.urls import path
from .views.autenticacion import *
from .views.views import *
from django.conf.urls.static import static
from .views.views import *
urlpatterns = [
    path('signUpPlan', signUpPlan.as_view(), name='signupPlan'),
    path('signUpDatos', signUpDatos.as_view(), name='signupDatos'),
    path('signUpPago', signUpPago.as_view(), name='signupPago'),
    path('perfil', perfil.as_view(), name='perfil'),
    path('logIn', logIn.as_view(), name='login'),
    path('logOut', logOut.as_view(), name='logout'),
    path('progreso/', progreso.as_view(), name='progreso'),
    path('entrenamiento', entrenamiento.as_view(), name='entrenamiento'),
    path('entrenamiento/rutina/<str:sitio>/', rutina.as_view(), name='rutina'),
    path('progreso/datosFisicos', datosFisicos.as_view(), name='datos_fisicos'),
    path('peso-data/', PesoDataView.as_view(), name='peso_data'),

]