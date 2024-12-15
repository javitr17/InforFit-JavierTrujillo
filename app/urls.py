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
    path('peso-diario/', PesoDiarioView.as_view(), name='peso_diario'),
    path('peso-data/', PesoDataView.as_view(), name='peso_data'),
    path('entrenamiento', entrenamiento.as_view(), name='entrenamiento'),
    path('rutina/<str:sitio>/', rutina.as_view(), name='rutina'),
]