from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms import Textarea

from markdownfield.forms import MarkdownFormField
from markdownfield.models import MarkdownField
from markdownfield.validators import VALIDATOR_BASIC
from markdownfield.widgets import MDEAdminWidget, MDEWidget


class TestMarkdownFormField:
    # formfield() returns MarkdownFormField by default
    def test_formfield_returns_markdown_form_field(self):
        field = MarkdownField(rendered_field=None)
        form_field = field.formfield()
        assert isinstance(form_field, MarkdownFormField)

    # formfield() uses MDEWidget when use_editor=True
    def test_formfield_uses_mde_widget(self):
        field = MarkdownField(rendered_field=None)
        form_field = field.formfield()
        assert isinstance(form_field.widget, MDEWidget)

    # use_editor=False with use_admin_editor=False gives standard Textarea
    def test_use_editor_false_skips_widget(self):
        field = MarkdownField(rendered_field=None, use_editor=False, use_admin_editor=False)
        form_field = field.formfield()
        assert isinstance(form_field.widget, Textarea)
        assert not isinstance(form_field.widget, MDEWidget)


class TestAdminWidget:
    # formfield() uses MDEAdminWidget when admin passes AdminTextareaWidget
    def test_admin_widget_replaces_textarea(self):
        field = MarkdownField(rendered_field=None)
        form_field = field.formfield(widget=AdminTextareaWidget)
        assert isinstance(form_field.widget, MDEAdminWidget)

    # non-admin formfield() call gets MDEWidget, not MDEAdminWidget
    def test_non_admin_does_not_get_admin_widget(self):
        field = MarkdownField(rendered_field=None)
        form_field = field.formfield()
        assert isinstance(form_field.widget, MDEWidget)
        assert not isinstance(form_field.widget, MDEAdminWidget)

    # use_admin_editor=False keeps AdminTextareaWidget
    def test_admin_editor_false_keeps_textarea(self):
        field = MarkdownField(rendered_field=None, use_admin_editor=False)
        form_field = field.formfield(widget=AdminTextareaWidget)
        assert isinstance(form_field.widget, AdminTextareaWidget)
        assert not isinstance(form_field.widget, MDEAdminWidget)

    # MDEAdminWidget receives the correct validator_name
    def test_admin_widget_passes_validator_name(self):
        field = MarkdownField(rendered_field=None, validator=VALIDATOR_BASIC)
        form_field = field.formfield(widget=AdminTextareaWidget)
        assert form_field.widget.validator_name == 'basic'


class TestMDEWidget:
    # two widget instances have different UUIDs
    def test_unique_uuid_per_instance(self):
        w1 = MDEWidget()
        w2 = MDEWidget()
        assert w1.uuid != w2.uuid

    # widget media includes EasyMDE JS and CSS
    def test_widget_media_includes_easymde(self):
        w = MDEWidget()
        media_js = str(w.media['js'])
        media_css = str(w.media['css'])
        assert 'easymde.min.js' in media_js
        assert 'easymde.min.css' in media_css
