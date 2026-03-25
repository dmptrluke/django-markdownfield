from django.test import override_settings

import pytest

from markdownfield.rendering import render_markdown
from markdownfield.validators import VALIDATOR_NULL

pytestmark = pytest.mark.django_db


class TestRenderingPipeline:
    # empty string input returns empty string
    def test_empty_string_returns_empty(self):
        assert render_markdown('') == ''

    # None input returns empty string
    def test_none_returns_empty(self):
        assert render_markdown(None) == ''

    # basic markdown syntax converts to HTML
    def test_basic_markdown_to_html(self):
        result = render_markdown('# Heading\n\n**bold** and *italic*')
        assert '<h1>Heading</h1>' in result
        assert '<strong>bold</strong>' in result
        assert '<em>italic</em>' in result

    # fenced code blocks work with default extensions
    def test_fenced_code_blocks(self):
        result = render_markdown('```python\nprint("hi")\n```')
        assert '<code' in result
        assert 'print' in result

    # script tags are stripped (content removed via clean_content_tags)
    def test_script_tags_stripped(self):
        result = render_markdown('<script>alert("xss")</script>safe')
        assert '<script>' not in result
        assert 'alert' not in result
        assert 'safe' in result

    # onclick attributes are stripped
    def test_onclick_attrs_stripped(self):
        result = render_markdown('<div onclick="alert(1)">text</div>')
        assert 'onclick' not in result
        assert 'text' in result

    # img onerror attributes are stripped
    def test_img_onerror_stripped(self):
        result = render_markdown('<img src="x" onerror="alert(1)">')
        assert 'onerror' not in result

    # javascript: URIs are stripped from links
    def test_javascript_uri_stripped(self):
        result = render_markdown('[click](javascript:alert(1))')
        assert 'javascript:' not in result

    # nofollow/noopener/noreferrer applied to links
    def test_link_rel_applied(self):
        result = render_markdown('[link](https://example.com)')
        assert 'rel="nofollow noopener noreferrer"' in result

    # VALIDATOR_NULL skips sanitization entirely
    def test_unsanitized_with_null_validator(self):
        result = render_markdown('<script>alert(1)</script>', VALIDATOR_NULL)
        assert '<script>' in result


class TestRenderingSettings:
    # MARKDOWN_EXTENSIONS setting adds extensions
    @override_settings(MARKDOWN_EXTENSIONS=['fenced_code', 'tables'])
    def test_custom_extensions_from_settings(self):
        table = '| a | b |\n|---|---|\n| 1 | 2 |'
        result = render_markdown(table, VALIDATOR_NULL)
        assert '<table>' in result

    # MARKDOWN_EXTENSION_CONFIGS passes through to markdown
    @override_settings(
        MARKDOWN_EXTENSIONS=['fenced_code', 'toc'],
        MARKDOWN_EXTENSION_CONFIGS={'toc': {'permalink': True}},
    )
    def test_custom_extension_configs(self):
        result = render_markdown('# Heading')
        assert 'id=' in result
