from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_image, name='upload_image'),
    path('show/', views.show_image, name='show_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)