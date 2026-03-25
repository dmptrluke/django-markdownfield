from django.conf import settings

import nh3
from markdown import markdown

from .util import process_links
from .validators import VALIDATOR_STANDARD


def render_markdown(text, validator=VALIDATOR_STANDARD):
    """Render markdown text to sanitized HTML.

    Pipeline: source text -> markdown() -> nh3.clean() -> process_links() -> HTML
    When validator.sanitize is False, nh3.clean() and process_links() are skipped.
    """
    if not text:
        return ''

    extensions = getattr(settings, 'MARKDOWN_EXTENSIONS', ['fenced_code'])
    extension_configs = getattr(settings, 'MARKDOWN_EXTENSION_CONFIGS', {})

    dirty = markdown(text=text, extensions=extensions, extension_configs=extension_configs)

    if validator.sanitize:
        clean = nh3.clean(
            dirty,
            tags=validator.allowed_tags,
            attributes=validator.allowed_attrs,
            clean_content_tags={'script', 'style'},
            link_rel='nofollow noopener noreferrer',
            filter_style_properties=validator.filter_style_properties,
            generic_attribute_prefixes=validator.generic_attribute_prefixes,
            url_schemes=validator.url_schemes,
        )
        return process_links(clean)

    return dirty
