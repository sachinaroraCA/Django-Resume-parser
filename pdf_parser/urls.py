from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

from . import views
app_name = 'pdf_parser'

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^dataparsing/$', views.dataparsing, name='dataparsing'),
    url('^resumeinformation/$', views.resumeinformation, name='resumeinformation'),
    url(r'^resume_data_delete/$',views.resume_data_delete,name='resume_data_delete'),
]

