import nh3

from .backends import get_backend
from .util import process_links
from .validators import VALIDATOR_STANDARD

_CLEAN_CONTENT_TAGS = {'script', 'style', 'iframe'}


def render_markdown(text, validator=VALIDATOR_STANDARD):
    """Render markdown text to sanitized HTML.

    Pipeline: source text -> backend() -> nh3.clean() -> process_links() -> HTML
    When validator.sanitize is False, nh3.clean() and process_links() are skipped.
    """
    if not text:
        return ''

    backend = get_backend()
    dirty = backend(text)

    if validator.sanitize:
        clean = nh3.clean(
            dirty,
            tags=validator.allowed_tags,
            attributes=validator.allowed_attrs,
            clean_content_tags=_CLEAN_CONTENT_TAGS - validator.allowed_tags,
            link_rel='nofollow noopener noreferrer',
            filter_style_properties=validator.filter_style_properties,
            generic_attribute_prefixes=validator.generic_attribute_prefixes,
            url_schemes=validator.url_schemes,
        )
        return process_links(clean)

    return dirty
