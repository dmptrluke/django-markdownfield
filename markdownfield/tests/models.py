from django.db import models

from markdownfield.models import MarkdownField, RenderedMarkdownField


class SamplePost(models.Model):
    body = MarkdownField(rendered_field='body_rendered')
    body_rendered = RenderedMarkdownField()

    class Meta:
        app_label = 'tests'

    def __str__(self):
        return f'SamplePost {self.pk}'


class SampleStandalonePost(models.Model):
    body = MarkdownField(rendered_field=None)

    class Meta:
        app_label = 'tests'

    def __str__(self):
        return f'SampleStandalonePost {self.pk}'
