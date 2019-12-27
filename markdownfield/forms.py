from django.forms import CharField

from .widgets import MDEWidget


class MarkdownFormField(CharField):
    widget = MDEWidget
