from django.test import override_settings

from markdownfield.util import process_links


class TestExternalLinkMarking:
    # external links get target=_blank and class=external
    @override_settings(MARKDOWNFIELD_INTERNAL_URL='https://example.com', MARKDOWNFIELD_MARK_EXTERNAL_LINKS=True)
    def test_external_link_marked(self):
        html = '<a href="https://other.com">link</a>'
        result = process_links(html)
        assert 'target="_blank"' in result
        assert 'class="external"' in result

    # links matching MARKDOWNFIELD_INTERNAL_URL are left alone
    @override_settings(MARKDOWNFIELD_INTERNAL_URL='https://example.com', MARKDOWNFIELD_MARK_EXTERNAL_LINKS=True)
    def test_internal_link_not_marked(self):
        html = '<a href="https://example.com/page">link</a>'
        result = process_links(html)
        assert 'target="_blank"' not in result
        assert 'external' not in result

    # fragment-only links (#anchor) are not marked as external
    @override_settings(MARKDOWNFIELD_INTERNAL_URL='https://example.com', MARKDOWNFIELD_MARK_EXTERNAL_LINKS=True)
    def test_fragment_link_not_marked(self):
        html = '<a href="#section">link</a>'
        result = process_links(html)
        assert 'external' not in result

    # links with no netloc (relative paths) are not marked
    @override_settings(MARKDOWNFIELD_INTERNAL_URL='https://example.com', MARKDOWNFIELD_MARK_EXTERNAL_LINKS=True)
    def test_relative_link_not_marked(self):
        html = '<a href="/page">link</a>'
        result = process_links(html)
        assert 'external' not in result

    # without MARKDOWNFIELD_INTERNAL_URL, all links with a netloc are treated as external
    @override_settings(MARKDOWNFIELD_INTERNAL_URL=None, MARKDOWNFIELD_MARK_EXTERNAL_LINKS=True)
    def test_no_site_url_all_external(self):
        html = '<a href="https://example.com">link</a>'
        result = process_links(html)
        assert 'class="external"' in result

    # external link with existing class gets "external" appended
    @override_settings(MARKDOWNFIELD_INTERNAL_URL='https://example.com', MARKDOWNFIELD_MARK_EXTERNAL_LINKS=True)
    def test_existing_class_appended(self):
        html = '<a href="https://other.com" class="button">link</a>'
        result = process_links(html)
        assert 'class="button external"' in result

    # MARKDOWNFIELD_MARK_EXTERNAL_LINKS=False disables marking
    @override_settings(MARKDOWNFIELD_MARK_EXTERNAL_LINKS=False, MARKDOWNFIELD_BLOCKED_LINK_DOMAINS=[])
    def test_external_marking_disabled(self):
        html = '<a href="https://other.com">link</a>'
        result = process_links(html)
        assert 'external' not in result


class TestBlockedDomains:
    # blocked domain links are stripped, text preserved
    @override_settings(MARKDOWNFIELD_BLOCKED_LINK_DOMAINS=['evil.com'], MARKDOWNFIELD_MARK_EXTERNAL_LINKS=False)
    def test_blocked_domain_stripped(self):
        html = '<a href="https://evil.com/page">visible text</a>'
        result = process_links(html)
        assert '<a ' not in result
        assert 'visible text' in result

    # non-blocked links are kept
    @override_settings(MARKDOWNFIELD_BLOCKED_LINK_DOMAINS=['evil.com'], MARKDOWNFIELD_MARK_EXTERNAL_LINKS=False)
    def test_non_blocked_link_kept(self):
        html = '<a href="https://good.com">link</a>'
        result = process_links(html)
        assert '<a ' in result
