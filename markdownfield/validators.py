from dataclasses import dataclass
from typing import List

import bleach_whitelist


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
    allowed_tags=bleach_whitelist.markdown_tags + ['pre', 'dl', 'del', 'abbr'],
    allowed_attrs={
        **bleach_whitelist.markdown_attrs,
        'abbr': ['title']
    },
    sanitize=True
)

VALIDATOR_CLASSY = Validator(
    allowed_tags=bleach_whitelist.markdown_tags + ['pre', 'dl', 'del', 'abbr'],
    allowed_attrs={
        **bleach_whitelist.markdown_attrs,
        'abbr': ['title'],
        'img': ['src', 'alt', 'title', 'class'],
        'a': ['href', 'alt', 'title', 'name', 'class']
    },
    sanitize=True
)
