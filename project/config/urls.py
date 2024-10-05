from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from miapp.views import HomeView  
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  
    path('', HomeView.as_view(), name='home'), 
    path('MR/', include('miapp.urls', namespace='miapp')),
    path('productos/', include('producto.urls', namespace='productos')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
