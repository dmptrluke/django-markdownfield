from django.db.models import TextField
from django.utils.safestring import mark_safe

from .forms import MarkdownFormField
from .rendering import render_markdown
from .validators import VALIDATOR_STANDARD, Validator
from .widgets import MDEAdminWidget, MDEWidget


class RenderedMarkdownField(TextField):
    """
    RenderedMarkdownField is pretty much just a plain textfield that doesn't show up in the admin panel.

    Using a custom field type also allows more functionality (eg; custom display rules, automatic mark_safe)
    to be added in the future.
    """

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        kwargs['blank'] = False
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return mark_safe(value)  # noqa: S308

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['editable']
        return name, path, args, kwargs


class MarkdownField(TextField):
    def __init__(
        self,
        *args,
        rendered_field: str | None = None,
        validator: Validator = VALIDATOR_STANDARD,
        use_editor: bool = True,
        use_admin_editor: bool = True,
        **kwargs,
    ):
        self.rendered_field = rendered_field
        self.use_editor = use_editor
        self.use_admin_editor = use_admin_editor
        self.validator = validator
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        # todo: deconstruct validators. maybe.
        name, path, args, kwargs = super().deconstruct()
        if self.rendered_field is not None:
            kwargs['rendered_field'] = self.rendered_field
        if self.use_editor is not True:
            kwargs['use_editor'] = self.use_editor
        if self.use_admin_editor is not True:
            kwargs['use_admin_editor'] = self.use_admin_editor
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {}
        if self.use_editor:
            defaults = {
                'form_class': MarkdownFormField,
                'widget': MDEWidget(validator_name=self.validator.name),
            }

        # detect admin context: ModelAdmin.formfield_for_dbfield passes
        # AdminTextareaWidget for TextFields
        from django.contrib.admin.widgets import AdminTextareaWidget

        widget_kwarg = kwargs.get('widget')
        is_admin = isinstance(widget_kwarg, type) and issubclass(widget_kwarg, AdminTextareaWidget)

        defaults.update(kwargs)

        if is_admin and self.use_admin_editor:
            defaults['widget'] = MDEAdminWidget(validator_name=self.validator.name)

        return super().formfield(**defaults)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if not self.rendered_field:
            return value

        setattr(model_instance, self.rendered_field, render_markdown(value, self.validator))
        return value
