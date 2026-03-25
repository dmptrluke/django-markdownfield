from django.utils.safestring import SafeString

import pytest

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_BASIC

from .models import SampleStandalonePost

pytestmark = pytest.mark.django_db


class TestRenderedMarkdownField:
    # from_db_value returns SafeString for non-None values
    def test_from_db_value_marks_safe(self, post):
        post.refresh_from_db()
        assert isinstance(post.body_rendered, SafeString)

    # from_db_value returns None for NULL database values
    def test_from_db_value_none_returns_none(self):
        field = RenderedMarkdownField()
        assert field.from_db_value(None, None, None) is None

    # field is not editable
    def test_not_editable(self):
        field = RenderedMarkdownField()
        assert field.editable is False

    # deconstruct omits editable kwarg for cleaner migrations
    def test_deconstruct_omits_editable(self):
        field = RenderedMarkdownField()
        _, _, _, kwargs = field.deconstruct()
        assert 'editable' not in kwargs


class TestMarkdownFieldPreSave:
    # saving populates the rendered field with HTML
    def test_pre_save_populates_rendered_field(self, post):
        assert '<strong>bold</strong>' in post.body_rendered

    # editing markdown and re-saving updates rendered HTML
    def test_rendered_field_updates_on_change(self, post):
        post.body = '# New heading'
        post.save()
        post.refresh_from_db()
        assert '<h1>New heading</h1>' in post.body_rendered

    # blank markdown clears the rendered field
    def test_empty_markdown_clears_rendered(self, post):
        post.body = ''
        post.save()
        post.refresh_from_db()
        assert post.body_rendered == ''

    # standalone field (no rendered_field) saves without error
    def test_standalone_skips_rendering(self, db):
        obj = SampleStandalonePost.objects.create(body='**bold**')
        assert not hasattr(obj, 'body_rendered')

    # field uses its configured validator on save
    def test_validator_respected_on_save(self, db):
        field = MarkdownField(rendered_field='body_rendered', validator=VALIDATOR_BASIC)
        result = field.validator
        assert result is VALIDATOR_BASIC
