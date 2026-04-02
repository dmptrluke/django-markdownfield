from dataclasses import dataclass, field

VALIDATORS = {}

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
    's',
    'sub',
    'sup',
    'table',
    'thead',
    'tbody',
    'tr',
    'th',
    'td',
}

MARKDOWN_ATTRS = {
    '*': {'id'},
    'img': {'src', 'alt', 'title', 'width', 'height'},
    'a': {'href', 'alt', 'title'},
    'abbr': {'title'},
    'th': {'style'},
    'td': {'style'},
}

MARKDOWN_URL_SCHEMES = {'http', 'https', 'mailto'}

TOOLBAR_FULL = [
    'bold',
    'italic',
    'strikethrough',
    '|',
    'heading-1',
    'heading-2',
    'heading-3',
    '|',
    'quote',
    'unordered-list',
    'ordered-list',
    '|',
    'code',
    'link',
    'image',
    'table',
    'horizontal-rule',
]


@dataclass
class Validator:
    """Define allowed tags, attributes, and toolbar for a markdown field."""

    allowed_tags: set[str]
    allowed_attrs: dict[str, set[str]]
    filter_style_properties: set[str] | None = None
    generic_attribute_prefixes: set[str] | None = None
    url_schemes: set[str] = field(default_factory=lambda: set(MARKDOWN_URL_SCHEMES))
    sanitize: bool = True
    name: str = 'custom'
    toolbar: list[str] = field(default_factory=lambda: list(TOOLBAR_FULL))

    def __post_init__(self):
        VALIDATORS[self.name] = self


VALIDATOR_STANDARD = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs=MARKDOWN_ATTRS,
    filter_style_properties={'text-align'},
    name='standard',
)

VALIDATOR_CLASSY = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        'img': {'src', 'alt', 'title', 'width', 'height', 'class'},
        'a': {'href', 'alt', 'title', 'name', 'class'},
    },
    filter_style_properties={'text-align'},
    generic_attribute_prefixes={'data-'},
    name='classy',
)

VALIDATOR_NO_IMAGES = Validator(
    allowed_tags=MARKDOWN_TAGS - {'img'},
    allowed_attrs={k: v for k, v in MARKDOWN_ATTRS.items() if k != 'img'},
    filter_style_properties={'text-align'},
    toolbar=[item for item in TOOLBAR_FULL if item != 'image'],
    name='no_images',
)

VALIDATOR_BASIC = Validator(
    allowed_tags={'b', 'i', 'strong', 'em', 'del', 's', 'code', 'p', 'br', 'a'},
    allowed_attrs={
        'a': {'href', 'alt', 'title'},
    },
    toolbar=[
        'bold',
        'italic',
        'code',
        '|',
        'link',
    ],
    name='basic',
)

VALIDATOR_NULL = Validator(allowed_tags=set(), allowed_attrs={}, sanitize=False, name='null')
