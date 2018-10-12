from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url('', include('pdf_parser.urls')),
    url('admin/', admin.site.urls),
]
