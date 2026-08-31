
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Necessário para o seletor de idioma do Jazzmin
    #path('i18n/', include('django.conf.urls.i18n')),

    path('', include('website.urls'))
]

# Só em desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
