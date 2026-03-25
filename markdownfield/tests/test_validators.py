from markdownfield.rendering import render_markdown
from markdownfield.validators import (
    MARKDOWN_TAGS,
    VALIDATOR_BASIC,
    VALIDATOR_CLASSY,
    VALIDATOR_NULL,
    VALIDATOR_STANDARD,
    VALIDATORS,
    Validator,
)


class TestValidatorStandard:
    # every tag in MARKDOWN_TAGS passes through standard validator
    def test_allows_all_markdown_tags(self):
        for tag in MARKDOWN_TAGS:
            html = f'<{tag}>content</{tag}>'
            result = render_markdown(html)
            # check for opening tag prefix (some tags get attrs injected by nh3)
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


class TestValidatorClassy:
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


class TestValidatorBasic:
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


class TestValidatorNull:
    # arbitrary HTML preserved when sanitize=False
    def test_allows_arbitrary_html(self):
        html = '<form><input type="text"><script>x</script></form>'
        result = render_markdown(html, VALIDATOR_NULL)
        assert '<form>' in result
        assert '<input' in result
        assert '<script>' in result


class TestCustomValidators:
    # custom validator auto-registers in VALIDATORS dict
    def test_custom_validator_registered(self):
        v = Validator(allowed_tags={'p'}, allowed_attrs={}, name='test_custom')
        assert VALIDATORS['test_custom'] is v

    # VALIDATORS lookup by name retrieves the correct instance
    def test_lookup_by_name(self):
        assert VALIDATORS['standard'] is VALIDATOR_STANDARD
        assert VALIDATORS['basic'] is VALIDATOR_BASIC
        assert VALIDATORS['classy'] is VALIDATOR_CLASSY
        assert VALIDATORS['null'] is VALIDATOR_NULL
