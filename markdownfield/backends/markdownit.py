from django.conf import settings
from django.utils.module_loading import import_string

from markdown_it import MarkdownIt

_allow_html = getattr(settings, 'MARKDOWNFIELD_ALLOW_HTML', True)
md = MarkdownIt('default', {'html': _allow_html})
md.enable('strikethrough')

for _plugin_path in getattr(settings, 'MARKDOWNFIELD_PLUGINS', []):
    _plugin = import_string(_plugin_path)
    _plugin(md)


def render(text):
    """Convert markdown source text to raw (unsanitized) HTML."""
    return md.render(text)
