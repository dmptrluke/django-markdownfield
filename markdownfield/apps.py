from django.apps import AppConfig
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.urls.exceptions import NoReverseMatch


class MarkdownFieldConfig(AppConfig):
    name = 'markdownfield'
    verbose_name = 'Markdown Field'

    def ready(self):
        checks.register(check_rendered_fields, checks.Tags.models)
        checks.register(check_preview_urls)


def check_rendered_fields(app_configs, **kwargs):
    from django.apps import apps

    from .models import MarkdownField

    errors = []
    models = apps.get_models() if app_configs is None else [m for ac in app_configs for m in ac.get_models()]
    for model in models:
        for field in model._meta.get_fields():
            if isinstance(field, MarkdownField) and field.rendered_field:
                try:
                    model._meta.get_field(field.rendered_field)
                except FieldDoesNotExist:
                    errors.append(
                        checks.Warning(
                            f'{model.__name__}.{field.name} references rendered_field '
                            f'{field.rendered_field!r} which does not exist on the model.',
                            id='markdownfield.W001',
                        )
                    )
    return errors


def check_preview_urls(app_configs, **kwargs):
    try:
        from django.urls import reverse

        reverse('markdownfield:preview')
    except NoReverseMatch:
        return [
            checks.Warning(
                'markdownfield URLs are not included in your urlconf. '
                'Admin preview will not work. Add '
                "path('markdownfield/', include('markdownfield.urls')) to your root urlconf.",
                id='markdownfield.W002',
            )
        ]
    return []
