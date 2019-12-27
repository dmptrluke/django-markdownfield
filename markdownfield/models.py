from functools import partial

from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.db.models import TextField

import bleach
from bleach.linkifier import LinkifyFilter
from markdown import markdown

from .forms import MarkdownFormField
from .util import format_link
from .validators import VALIDATOR_STANDARD
from .widgets import MDEAdminWidget

ENABLE_EDITOR = getattr(settings, "MARKDOWN_EASYMDE", True)
ENABLE_ADMIN_EDITOR = getattr(settings, "MARKDOWN_ADMIN_EASYMDE", True)
EXTENSIONS = getattr(settings, 'MARKDOWN_EXTENSIONS', [])
EXTENSION_CONFIGS = getattr(settings, 'MARKDOWN_EXTENSION_CONFIGS', [])


class RenderedMarkdownField(TextField):
    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        kwargs['blank'] = False
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'


class MarkdownField(TextField):
    def __init__(self, *args, rendered_field=None, validator=VALIDATOR_STANDARD,
                 use_editor=ENABLE_EDITOR, use_admin_editor=ENABLE_ADMIN_EDITOR, **kwargs):
        self.rendered_field = rendered_field
        self.use_editor = use_editor
        self.use_admin_editor = use_admin_editor
        self.validator = validator
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'

    def formfield(self, **kwargs):
        defaults = {}
        if self.use_editor:
            defaults = {'form_class': MarkdownFormField}

        defaults.update(kwargs)

        if self.use_admin_editor:
            if defaults['widget'] == admin_widgets.AdminTextareaWidget:
                defaults['widget'] = MDEAdminWidget()

        return super().formfield(**defaults)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if not self.rendered_field:
            return value

        dirty = markdown(
            text=value,
            extensions=EXTENSIONS,
            extension_configs=EXTENSION_CONFIGS
        )

        if self.validator.sanitize:
            if self.validator.linkify:
                cleaner = bleach.Cleaner(tags=self.validator.allowed_tags,
                                         attributes=self.validator.allowed_attrs,
                                         filters=[partial(LinkifyFilter, callbacks=[format_link])])
            else:
                cleaner = bleach.Cleaner(tags=self.validator.allowed_tags,
                                         attributes=self.validator.allowed_attrs)

            clean = cleaner.clean(dirty)
            setattr(model_instance, self.rendered_field, clean)
        else:
            # danger!
            setattr(model_instance, self.rendered_field, dirty)

        return value
