from django.conf import settings

from markdown import markdown

_extensions = getattr(settings, 'MARKDOWN_EXTENSIONS', ['fenced_code'])
_extension_configs = getattr(settings, 'MARKDOWN_EXTENSION_CONFIGS', {})


def render(text):
    """Convert markdown source text to raw (unsanitized) HTML using python-markdown."""
    return markdown(text=text, extensions=_extensions, extension_configs=_extension_configs)
