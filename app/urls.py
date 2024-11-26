from django.urls import path
from .views.autenticacion import *
from .views.views import *

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('signUpPlan', signUpPlan.as_view(), name='signupPlan'),
    path('signUpDatos', signUpDatos.as_view(), name='signupDatos'),
    path('signUpPago', signUpPago.as_view(), name='signupPago'),
    path('charge', charge.as_view(), name='charge'),
    path('cancel', cancel.as_view(), name='cancel'),

    path('logIn', logIn.as_view(), name='login'),
    path('logOut', logOut.as_view(), name='logout'),

]