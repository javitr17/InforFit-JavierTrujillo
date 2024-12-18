from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Configura Django para usar Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InForFit.settings')

app = Celery('InForFit')

# Carga la configuración de Celery desde Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir automáticamente las tareas de todas las aplicaciones Django
app.autodiscover_tasks()

# Configuración de tareas periódicas con Celery Beat
app.conf.beat_schedule = {
    'procesar-pagos-diarios': {
        'task': 'app.tasks.procesar_pagos_diarios',  # Especificamos la tarea que queremos ejecutar
        'schedule': crontab(minute=0, hour=0),  # Ejecutar la tarea todos los días a medianoche
    },
}

# Asegúrate de que Celery se cargue correctamente cuando Django inicie
__all__ = ('app',)