from django.test import override_settings

import pytest

from markdownfield.backends import get_backend
from markdownfield.rendering import render_markdown


class TestBackendResolution:
    # default backend is markdownit when no setting is configured
    def test_default_backend_is_markdownit(self):
        backend = get_backend()
        assert backend.__module__ == 'markdownfield.backends.markdownit'

    # explicit MARKDOWNFIELD_BACKEND overrides the default
    @override_settings(MARKDOWNFIELD_BACKEND='markdownfield.backends.pymarkdown')
    def test_explicit_backend_override(self):
        backend = get_backend()
        assert backend.__module__ == 'markdownfield.backends.pymarkdown'

    # bad backend path raises ImportError
    @override_settings(MARKDOWNFIELD_BACKEND='nonexistent.module')
    def test_bad_backend_path_raises_import_error(self):
        with pytest.raises(ImportError):
            get_backend()

    # backend module without render() raises TypeError
    @override_settings(MARKDOWNFIELD_BACKEND='markdownfield.backends')
    def test_missing_render_raises_type_error(self):
        with pytest.raises(TypeError, match='must define a callable render'):
            get_backend()


class TestMarkdownItSettings:
    # MARKDOWNFIELD_ALLOW_HTML=False prevents raw HTML passthrough
    @override_settings(MARKDOWNFIELD_ALLOW_HTML=False)
    def test_allow_html_false_escapes_raw_html(self):
        result = render_markdown('<div>raw</div>')
        assert '<div>' not in result

    # MARKDOWNFIELD_PLUGINS loads plugins that modify rendering
    @override_settings(MARKDOWNFIELD_PLUGINS=['mdit_py_plugins.tasklists.tasklists_plugin'])
    def test_plugin_modifies_output(self):
        from markdownfield.validators import VALIDATOR_NULL

        result = render_markdown('- [ ] unchecked\n- [x] checked', VALIDATOR_NULL)
        assert 'type="checkbox"' in result


class TestPymarkdownBackend:
    # pymarkdown backend renders with python-markdown
    @override_settings(MARKDOWNFIELD_BACKEND='markdownfield.backends.pymarkdown')
    def test_renders_markdown(self):
        result = render_markdown('**bold** and *italic*')
        assert '<strong>bold</strong>' in result
        assert '<em>italic</em>' in result

    # MARKDOWN_EXTENSIONS setting adds extensions
    @override_settings(
        MARKDOWNFIELD_BACKEND='markdownfield.backends.pymarkdown',
        MARKDOWN_EXTENSIONS=['fenced_code', 'tables'],
    )
    def test_custom_extensions(self):
        from markdownfield.validators import VALIDATOR_NULL

        table = '| a | b |\n|---|---|\n| 1 | 2 |'
        result = render_markdown(table, VALIDATOR_NULL)
        assert '<table>' in result

    # MARKDOWN_EXTENSION_CONFIGS passes through to python-markdown
    @override_settings(
        MARKDOWNFIELD_BACKEND='markdownfield.backends.pymarkdown',
        MARKDOWN_EXTENSIONS=['fenced_code', 'toc'],
        MARKDOWN_EXTENSION_CONFIGS={'toc': {'permalink': True}},
    )
    def test_custom_extension_configs(self):
        result = render_markdown('# Heading')
        assert 'id=' in result
