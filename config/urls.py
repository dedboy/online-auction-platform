from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel manzili
    path('admin/', admin.site.urls),
    
    # Bizning auksion ilovamizning manzillari
    path('', include('auction.urls')),
]

# DEBUG rejimida media fayllarni (rasmlarni) ko'rsatish uchun ruxsat berish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)