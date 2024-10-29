from django.urls import path
from .views.autenticacion import *
from .views.views import *

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('signUp', signUp.as_view(), name='signup'),
    path('logIn', logIn.as_view(), name='login'),
    path('logOut', logOut.as_view(), name='logout'),

]