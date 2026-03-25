from django.template import Context, Template
from django.utils.safestring import SafeString

import pytest

from markdownfield.templatetags.markdownfield import render_markdown_filter


class TestRenderMarkdownFilter:
    # default (no arg) uses VALIDATOR_STANDARD
    def test_default_validator(self):
        result = render_markdown_filter('# Heading')
        assert '<h1>' in result

    # named validator changes filtering behavior
    def test_named_validator(self):
        result = render_markdown_filter('# Heading', 'basic')
        assert '<h1>' not in result

    # unknown validator name raises ValueError
    def test_unknown_validator_raises(self):
        with pytest.raises(ValueError, match='Unknown markdown validator'):
            render_markdown_filter('text', 'nonexistent')

    # return value is marked safe (nh3 already sanitized)
    def test_output_is_safe(self):
        result = render_markdown_filter('**bold**')
        assert isinstance(result, SafeString)

    # output is not auto-escaped in templates
    def test_output_not_escaped_in_template(self):
        template = Template('{% load markdownfield %}{{ text|render_markdown }}')
        result = template.render(Context({'text': '**bold**'}))
        assert '<strong>bold</strong>' in result
        assert '&lt;strong&gt;' not in result
