import re
from urllib.parse import urlparse

from django.conf import settings

BLACKLIST = getattr(settings, 'MARKDOWN_LINK_BLACKLIST', [])
MARK_EXTERNAL_LINKS = getattr(settings, 'MARKDOWN_MARK_EXTERNAL_LINKS', True)


def process_links(html: str) -> str:
    """Strip blacklisted links; optionally add target="_blank" and class="external" to external links."""
    if not BLACKLIST and not MARK_EXTERNAL_LINKS:
        return html

    if hasattr(settings, 'SITE_URL'):
        site_netloc = urlparse(settings.SITE_URL).netloc
    else:
        site_netloc = None

    if BLACKLIST:

        def strip_blacklisted(match: re.Match) -> str:
            href_match = re.search(r'href="([^"]*)"', match.group(0))
            if href_match and urlparse(href_match.group(1)).netloc in BLACKLIST:
                return match.group(1)
            return match.group(0)

        html = re.sub(r'<a\b[^>]*>(.*?)</a>', strip_blacklisted, html, flags=re.DOTALL)

    if not MARK_EXTERNAL_LINKS:
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

        link_is_external = p.netloc != site_netloc if site_netloc else True

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
