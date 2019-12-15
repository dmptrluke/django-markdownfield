from dataclasses import dataclass
from typing import List

MARKDOWN_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "b", "i", "strong", "em", "tt", "del", "abbr"
    "p", "br",
    "span", "div", "blockquote", "code", "pre", "hr",
    "ul", "dl", "ol", "li", "dd", "dt",
    "img",
    "a",
    "sub", "sup",
]

MARKDOWN_ATTRS = {
    "*": ["id"],
    "img": ["src", "alt", "title"],
    "a": ["href", "alt", "title"],
    "abbr": ["title"],
}


@dataclass
class Validator:
    """ defines a standard format for markdown validators """
    allowed_tags: List[str]
    allowed_attrs: dict
    sanitize: bool


VALIDATOR_NULL = Validator(
    allowed_tags=[],
    allowed_attrs={},
    sanitize=False
)

VALIDATOR_STANDARD = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs=MARKDOWN_ATTRS,
    sanitize=True
)

VALIDATOR_CLASSY = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        'img': ['src', 'alt', 'title', 'class'],
        'a': ['href', 'alt', 'title', 'name', 'class']
    },
    sanitize=True
)
