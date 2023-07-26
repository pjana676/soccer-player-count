from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import detect_people

urlpatterns = [
    path('api/detect-people/', detect_people, name='detect_people'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)