from django import template
from pdf_parser.models import *


register = template.Library()


@register.filter
def get_all_text(text):
        text = str(text)
        start = text[50:]
        return start

