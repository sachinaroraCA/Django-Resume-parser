from django.conf.urls import url,include
from django.views.static import serve
from django.conf import settings

from . import views
app_name = 'pdf_parser'
from pdf_parser.resource import NoteResource

note_resource = NoteResource()


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^dataparsing/$', views.dataparsing, name='dataparsing'),
    #url('^phone_api/$',views.phone_api,name = 'phone_api'),
    url('^resumeinformation/$', views.resumeinformation, name='resumeinformation'),
    url(r'^resume_data_delete/$',views.resume_data_delete,name='resume_data_delete'),
    url(r'^api/', include(note_resource.urls)),
]

