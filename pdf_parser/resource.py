from tastypie.resources import ModelResource
from pdf_parser.models import Note
from automationCTI.automationfx import *

class NoteResource(ModelResource):

    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        # sent_message = sendMessage('message', 'declaration')
