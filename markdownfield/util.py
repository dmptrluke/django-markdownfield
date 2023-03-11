from typing import Dict
from urllib.parse import urlparse

from django.conf import settings

BLACKLIST = getattr(settings, 'MARKDOWN_LINKIFY_BLACKLIST', [])


def blacklist_link(attrs: Dict[tuple, str], new: bool = False):
    try:
        p = urlparse(attrs[(None, 'href')])
    except KeyError:
        return attrs

    if (p.netloc in BLACKLIST) and new:
        return None
    return attrs


def format_link(attrs: Dict[tuple, str], new: bool = False):
    """
    This is really weird and ugly, but that's how bleach linkify filters work.
    """
    try:
        p = urlparse(attrs[(None, 'href')])
    except KeyError:
        # no href, probably an anchor
        return attrs

    if not any([p.scheme, p.netloc, p.path]) and p.fragment:
        # the link isn't going anywhere, probably a fragment link
        return attrs

    if hasattr(settings, 'SITE_URL'):
        c = urlparse(settings.SITE_URL)
        link_is_external = p.netloc != c.netloc
    else:
        # Assume true for safety
        link_is_external = True

    if link_is_external:
            # link is external - secure and mark
            attrs[(None, 'target')] = '_blank'
            attrs[(None, 'class')] = attrs.get((None, 'class'), '') + ' external'
            attrs[(None, 'rel')] = 'nofollow noopener noreferrer'

    return attrs
