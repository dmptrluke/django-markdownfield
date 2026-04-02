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

    # admin config includes preview when URL is provided
    def test_admin_widget_config_has_preview(self):
        w = MDEAdminWidget(preview_url='/preview/')
        ctx = w.get_context('body', '', {'id': 'id_body'})
        assert 'preview' in ctx['config']
        assert ctx['config']['preview']['url'] == '/preview/'
        assert ctx['config']['preview']['validator'] == 'standard'

    # admin config resolves preview URL from urlconf when not explicit
    def test_admin_widget_config_resolves_preview_url(self):
        w = MDEAdminWidget()
        ctx = w.get_context('body', '', {'id': 'id_body'})
        assert 'preview' in ctx['config']
        assert ctx['config']['preview']['url'] == '/markdownfield/preview/'

    # both widgets use the same template
    def test_both_widgets_use_same_template(self):
        assert MDEWidget.template_name == 'markdownfield/widget.html'
        assert MDEAdminWidget.template_name == 'markdownfield/widget.html'


class TestMDEWidget:
    # two widget instances have different UUIDs
    def test_unique_uuid_per_instance(self):
        w1 = MDEWidget()
        w2 = MDEWidget()
        assert w1.uuid != w2.uuid

    # widget media includes all JS files
    def test_widget_media_includes_js(self):
        w = MDEWidget()
        media_js = str(w.media['js'])
        assert 'easymde.min.js' in media_js
        assert 'markdownfield.js' in media_js
        assert 'mte-kernel.min.js' in media_js
        assert 'mte-plugin.js' in media_js

    # widget media includes all CSS files
    def test_widget_media_includes_css(self):
        w = MDEWidget()
        media_css = str(w.media['css'])
        assert 'easymde.min.css' in media_css
        assert 'md.css' in media_css

    # textarea gets data-markdownfield attribute pointing at config
    def test_widget_renders_data_attribute(self):
        w = MDEWidget()
        ctx = w.get_context('body', '', {'id': 'id_body'})
        assert 'data-markdownfield' in ctx['widget']['attrs']
        assert ctx['widget']['attrs']['data-markdownfield'] == w.config_id

    # config has toolbar and options but no preview
    def test_widget_config_shape(self):
        w = MDEWidget()
        ctx = w.get_context('body', '', {'id': 'id_body'})
        config = ctx['config']
        assert 'toolbar' in config
        assert 'options' in config
        assert 'preview' not in config

    # config toolbar reflects validator (basic excludes table)
    def test_widget_config_toolbar_from_validator(self):
        w = MDEWidget(validator_name='basic')
        ctx = w.get_context('body', '', {'id': 'id_body'})
        assert 'bold' in ctx['config']['toolbar']
        assert 'table' not in ctx['config']['toolbar']
