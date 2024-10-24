
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='InForFit/index.html'), name='welcome'),
    path('InForFit/', include('app.urls')),
]
