from django.conf import settings
from django.utils.module_loading import import_string

from markdown_it import MarkdownIt

md = MarkdownIt(
    'default',
    {
        'html': getattr(settings, 'MARKDOWNFIELD_ALLOW_HTML', True),
        'linkify': getattr(settings, 'MARKDOWNFIELD_LINKIFY', False),
        'typographer': getattr(settings, 'MARKDOWNFIELD_TYPOGRAPHER', False),
        'breaks': getattr(settings, 'MARKDOWNFIELD_BREAKS', False),
    },
)
md.enable('strikethrough')

for _plugin_path in getattr(settings, 'MARKDOWNFIELD_PLUGINS', []):
    _plugin = import_string(_plugin_path)
    _plugin(md)


def render(text):
    """Convert markdown source text to raw (unsanitized) HTML."""
    return md.render(text)
