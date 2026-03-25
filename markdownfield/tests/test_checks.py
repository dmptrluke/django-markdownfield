from django.test import override_settings

import pytest

from markdownfield.apps import check_preview_urls, check_rendered_fields

pytestmark = pytest.mark.django_db


class TestRenderedFieldCheck:
    # warns when rendered_field references a nonexistent field
    def test_missing_rendered_field_warns(self):

        from .models import SamplePost

        original = SamplePost._meta.get_field('body').rendered_field
        try:
            SamplePost._meta.get_field('body').rendered_field = 'nonexistent'
            errors = check_rendered_fields(app_configs=None)
            warning_ids = [e.id for e in errors]
            assert 'markdownfield.W001' in warning_ids
        finally:
            SamplePost._meta.get_field('body').rendered_field = original

    # no warning when rendered_field config is valid
    def test_valid_rendered_field_no_warning(self):
        errors = check_rendered_fields(app_configs=None)
        warning_ids = [e.id for e in errors]
        assert 'markdownfield.W001' not in warning_ids


class TestPreviewUrlCheck:
    # warns when markdownfield:preview URL is not registered
    @override_settings(ROOT_URLCONF='markdownfield.tests.empty_urls')
    def test_missing_preview_url_warns(self):
        errors = check_preview_urls(app_configs=None)
        warning_ids = [e.id for e in errors]
        assert 'markdownfield.W002' in warning_ids

    # no warning when preview URL is registered
    def test_preview_url_present_no_warning(self):
        errors = check_preview_urls(app_configs=None)
        assert len(errors) == 0
