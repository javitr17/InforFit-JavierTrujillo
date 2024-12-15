
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from .viewsBase.viewsBase import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.as_view(), name='welcome'),
    path('InForFit/', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
