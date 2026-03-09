from dataclasses import dataclass

MARKDOWN_TAGS = {
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'b',
    'i',
    'strong',
    'em',
    'tt',
    'del',
    'abbr',
    'p',
    'br',
    'span',
    'div',
    'blockquote',
    'code',
    'pre',
    'hr',
    'ul',
    'dl',
    'ol',
    'li',
    'dd',
    'dt',
    'img',
    'a',
    'sub',
    'sup',
}

MARKDOWN_ATTRS = {
    '*': {'id'},
    'img': {'src', 'alt', 'title'},
    'a': {'href', 'alt', 'title'},
    'abbr': {'title'},
}


@dataclass
class Validator:
    """defines a standard format for markdown validators"""

    allowed_tags: set[str]
    allowed_attrs: dict[str, set[str]]
    filter_style_properties: set[str] | None = None
    generic_attribute_prefixes: set[str] | None = None
    url_schemes: set[str] | None = None
    sanitize: bool = True


VALIDATOR_NULL = Validator(allowed_tags=set(), allowed_attrs={}, sanitize=False)

VALIDATOR_STANDARD = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs=MARKDOWN_ATTRS,
)

VALIDATOR_CLASSY = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        'img': {'src', 'alt', 'title', 'class'},
        'a': {'href', 'alt', 'title', 'name', 'class'},
    },
    generic_attribute_prefixes={'data-'},
)
