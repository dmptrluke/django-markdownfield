import re
from urllib.parse import urlparse

from django.conf import settings


def process_links(html: str) -> str:
    """Strip blocked domain links; optionally add target="_blank" and class="external" to external links."""
    blocked_domains = getattr(
        settings,
        'MARKDOWNFIELD_BLOCKED_LINK_DOMAINS',
        getattr(settings, 'MARKDOWN_LINK_BLACKLIST', []),
    )
    mark_external_links = getattr(
        settings,
        'MARKDOWNFIELD_MARK_EXTERNAL_LINKS',
        getattr(settings, 'MARKDOWN_MARK_EXTERNAL_LINKS', True),
    )
    internal_urls = getattr(
        settings,
        'MARKDOWNFIELD_INTERNAL_URL',
        getattr(settings, 'SITE_URL', None),
    )

    if not blocked_domains and not mark_external_links:
        return html

    if internal_urls is None:
        internal_netlocs = set()
    elif isinstance(internal_urls, str):
        internal_netlocs = {urlparse(internal_urls).netloc}
    else:
        internal_netlocs = {urlparse(u).netloc for u in internal_urls}

    if blocked_domains:

        def strip_blocked_domainsed(match: re.Match) -> str:
            href_match = re.search(r'href="([^"]*)"', match.group(0))
            if href_match and urlparse(href_match.group(1)).netloc in blocked_domains:
                return match.group(1)
            return match.group(0)

        html = re.sub(r'<a\b[^>]*>(.*?)</a>', strip_blocked_domainsed, html, flags=re.DOTALL)

    if not mark_external_links:
        return html

    def mark_external(match: re.Match) -> str:
        tag = match.group(0)
        href_match = re.search(r'href="([^"]*)"', tag)
        if not href_match:
            return tag

        p = urlparse(href_match.group(1))

        if not any([p.scheme, p.netloc, p.path]) and p.fragment:
            return tag

        if not p.netloc:
            return tag

        link_is_external = p.netloc not in internal_netlocs if internal_netlocs else True

        if not link_is_external:
            return tag

        if 'target=' not in tag:
            tag = tag[:-1] + ' target="_blank">'

        if 'class=' in tag:
            tag = re.sub(r'class="([^"]*)"', r'class="\1 external"', tag)
        else:
            tag = tag[:-1] + ' class="external">'

        return tag

    return re.sub(r'<a\b[^>]*>', mark_external, html)
