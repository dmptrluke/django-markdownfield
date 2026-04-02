import pytest

from markdownfield.rendering import render_markdown
from markdownfield.validators import (
    MARKDOWN_TAGS,
    VALIDATOR_BASIC,
    VALIDATOR_CLASSY,
    VALIDATOR_NO_IMAGES,
    VALIDATOR_NULL,
    VALIDATOR_STANDARD,
    Validator,
)

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

    # style tags are stripped (content removed via clean_content_tags)
    def test_style_tags_stripped(self):
        result = render_markdown('<style>body{display:none}</style>visible')
        assert '<style>' not in result
        assert 'display:none' not in result
        assert 'visible' in result

    # iframe content is fully removed, not just the tag
    def test_iframe_content_stripped(self):
        result = render_markdown('<iframe><script>alert(1)</script></iframe>safe')
        assert '<iframe>' not in result
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

    # javascript: URIs are not rendered as links
    def test_javascript_uri_stripped(self):
        result = render_markdown('[click](javascript:alert(1))')
        assert 'href="javascript:' not in result

    # nofollow/noopener/noreferrer applied to links
    def test_link_rel_applied(self):
        result = render_markdown('[link](https://example.com)')
        assert 'rel="nofollow noopener noreferrer"' in result

    # VALIDATOR_NULL skips sanitization entirely
    def test_unsanitized_with_null_validator(self):
        result = render_markdown('<script>alert(1)</script>', VALIDATOR_NULL)
        assert '<script>' in result


class TestStandardValidatorRendering:
    # every tag in MARKDOWN_TAGS passes through standard validator
    def test_allows_all_markdown_tags(self):
        # table-inner tags need table context (nh3 strips orphaned table elements per HTML5)
        table_inner = {'thead', 'tbody', 'tr', 'th', 'td'}
        for tag in MARKDOWN_TAGS - table_inner:
            html = f'<{tag}>content</{tag}>'
            result = render_markdown(html)
            assert f'<{tag}' in result, f'{tag} should be allowed'

    # table tags pass through when used with proper table structure
    def test_allows_table_tags(self):
        html = '<table><thead><tr><th>h</th></tr></thead><tbody><tr><td>d</td></tr></tbody></table>'
        result = render_markdown(html)
        for tag in ('table', 'thead', 'tbody', 'tr', 'th', 'td'):
            assert f'<{tag}' in result, f'{tag} should be allowed'

    # tags not in MARKDOWN_TAGS are stripped
    def test_strips_disallowed_tags(self):
        for tag in ('form', 'input', 'iframe', 'object'):
            result = render_markdown(f'<{tag}>content</{tag}>')
            assert f'<{tag}>' not in result, f'{tag} should be stripped'

    # img attributes: src, alt, title, width, height allowed
    def test_allows_img_attrs(self):
        html = '<img src="test.jpg" alt="test" title="t" width="100" height="50">'
        result = render_markdown(html)
        for attr in ('src=', 'alt=', 'title=', 'width=', 'height='):
            assert attr in result, f'{attr} should be allowed on img'

    # link attributes: href, alt, title allowed
    def test_allows_link_attrs(self):
        result = render_markdown('[link](https://example.com "title")')
        assert 'href=' in result
        assert 'title=' in result

    # standard validator strips data-* attributes (only classy allows them)
    def test_strips_data_attributes(self):
        result = render_markdown('<a href="#" data-tooltip="hi">link</a>', VALIDATOR_STANDARD)
        assert 'data-tooltip' not in result

    # url_schemes restricts allowed protocols
    def test_url_schemes_restricts_protocols(self):
        strict = Validator(
            allowed_tags={'a'},
            allowed_attrs={'a': {'href'}},
            url_schemes={'https'},
            name='test_strict_schemes',
        )
        result = render_markdown('<a href="http://example.com">link</a>', strict)
        assert 'href="http://example.com"' not in result

    # strikethrough renders correctly (markdownit uses <s> tag)
    def test_renders_strikethrough(self):
        result = render_markdown('~~deleted~~')
        assert '<s>' in result
        assert 'deleted' in result

    # table alignment style survives nh3 sanitization
    def test_table_alignment_survives_sanitization(self):
        table = '| left | center | right |\n|:-----|:------:|------:|\n| a | b | c |'
        result = render_markdown(table)
        assert 'text-align:center' in result or 'text-align: center' in result


class TestClassyValidatorRendering:
    # class attribute allowed on img and a
    def test_allows_class_on_img_and_link(self):
        img_result = render_markdown('<img src="t.jpg" class="hero">', VALIDATOR_CLASSY)
        assert 'class="hero"' in img_result

        link_result = render_markdown('<a href="#" class="btn">click</a>', VALIDATOR_CLASSY)
        assert 'class=' in link_result

    # data-* attributes allowed
    def test_allows_data_attributes(self):
        result = render_markdown('<a href="#" data-tooltip="hi">link</a>', VALIDATOR_CLASSY)
        assert 'data-tooltip=' in result


class TestBasicValidatorRendering:
    # block elements (headers, lists, images) stripped
    def test_strips_block_elements(self):
        result = render_markdown('# Heading\n\n- list item\n\n![img](test.jpg)', VALIDATOR_BASIC)
        assert '<h1>' not in result
        assert '<li>' not in result
        assert '<img' not in result

    # inline formatting preserved
    def test_allows_inline_only(self):
        result = render_markdown('**bold** *italic* `code` [link](https://example.com)', VALIDATOR_BASIC)
        assert '<strong>' in result
        assert '<em>' in result
        assert '<code>' in result
        assert '<a ' in result


class TestNullValidatorRendering:
    # arbitrary HTML preserved when sanitize=False
    def test_allows_arbitrary_html(self):
        html = '<form><input type="text"><script>x</script></form>'
        result = render_markdown(html, VALIDATOR_NULL)
        assert '<form>' in result
        assert '<input' in result
        assert '<script>' in result


class TestNoImagesValidatorRendering:
    # images are stripped
    def test_strips_images(self):
        result = render_markdown('![alt](test.jpg)', VALIDATOR_NO_IMAGES)
        assert '<img' not in result

    # other standard tags still work
    def test_allows_standard_tags(self):
        result = render_markdown('# Heading\n\n**bold** [link](https://example.com)', VALIDATOR_NO_IMAGES)
        assert '<h1>' in result
        assert '<strong>' in result
        assert '<a ' in result

    # tables still work
    def test_allows_tables(self):
        table = '| a | b |\n|---|---|\n| 1 | 2 |'
        result = render_markdown(table, VALIDATOR_NO_IMAGES)
        assert '<table>' in result
