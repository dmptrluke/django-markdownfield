from django import template

from ..rendering import render_markdown
from ..validators import VALIDATORS

register = template.Library()


@register.filter(name='render_markdown', is_safe=True)
def render_markdown_filter(value, validator_name='standard'):
    """Render markdown text to sanitized HTML using a named validator."""
    validator = VALIDATORS.get(validator_name)
    if validator is None:
        raise ValueError(f'Unknown markdown validator: {validator_name!r}')
    return render_markdown(value, validator)
