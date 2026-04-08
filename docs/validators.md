# Validators

Validators control HTML sanitization. Each `MarkdownField` takes a
`validator` argument that determines which tags, attributes.

If no custom toolbar is configured, the validator chosen will also control
which toolbar buttons are shown in the editor (hiding buttons for features
which are blocked)

## Built-in validators

### VALIDATOR_STANDARD

The default. Allows headings, paragraphs, inline formatting (`strong`, `em`, `del`, `s`, `code`,
`sub`, `sup`), block elements (`blockquote`, `pre`, `hr`, `div`, `span`), lists (`ul`, `ol`, `li`,
`dl`, `dt`, `dd`), tables (`table`, `thead`, `tbody`, `tr`, `th`, `td`), links, and images. Table
cell alignment via `style="text-align:..."` is preserved.

```python
from markdownfield.validators import VALIDATOR_STANDARD

text = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD)
```

### VALIDATOR_CLASSY

Extends VALIDATOR_STANDARD with `class` attributes on links and images, and `data-*` attributes on
all elements.

```python
from markdownfield.validators import VALIDATOR_CLASSY

text = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_CLASSY)
```

### VALIDATOR_NO_IMAGES

Everything in VALIDATOR_STANDARD except images. For user-generated content where you want full 
formatting but not image embedding.

```python
from markdownfield.validators import VALIDATOR_NO_IMAGES
```

### VALIDATOR_BASIC

Inline formatting only: `b`, `i`, `strong`, `em`, `del`, `s`, `code`, `p`, `br`, and `a`. Block
elements (headings, lists, images, tables) are stripped.

```python
from markdownfield.validators import VALIDATOR_BASIC
```

### VALIDATOR_NULL

Skips sanitization entirely. Arbitrary HTML passes through unchanged, including `<script>` tags. Any
user who can edit this field can execute JavaScript in the browser of anyone who views the rendered 
output. **Do not use unless you fully control all content.**

```python
from markdownfield.validators import VALIDATOR_NULL
```

## Creating custom validators

Create an instance of the `Validator` dataclass:

```python
from markdownfield.validators import Validator

VALIDATOR_COMMENTS = Validator(
    allowed_tags={'b', 'i', 'strong', 'em', 'p', 'br', 'a'},
    allowed_attrs={
        'a': {'href', 'title'},
    },
    name='comments',
)
```

### Extending built-in tag sets

```python
from markdownfield.validators import Validator, MARKDOWN_TAGS, MARKDOWN_ATTRS

VALIDATOR_CUSTOM = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        'img': {'src', 'alt', 'title', 'class'},
        'a': {'href', 'alt', 'title', 'name', 'class'},
    },
    generic_attribute_prefixes={'data-'},
    name='custom',
)
```

### Allowing inline CSS

Add `style` to `allowed_attrs` for the relevant tags and use `filter_style_properties` to restrict
which CSS properties are permitted:

```python
VALIDATOR_STYLED = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        '*': {'id', 'style'},
    },
    filter_style_properties={'color', 'font-weight', 'text-align'},
    name='styled',
)
```

`filter_style_properties` only applies to tags that have `style` in their `allowed_attrs`. If
`style` is allowed but `filter_style_properties` is not set, all CSS properties pass through.

### URL schemes

Built-in validators allow `http`, `https`, and `mailto` links by default (`MARKDOWN_URL_SCHEMES`).
To widen or narrow this:

```python
VALIDATOR_WITH_TEL = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs=MARKDOWN_ATTRS,
    url_schemes={'http', 'https', 'mailto', 'tel'},
    name='with_tel',
)
```

### Custom toolbar

Each validator has a `toolbar` field that controls which EasyMDE buttons appear. It defaults to
`TOOLBAR_FULL`. Override it to match what your validator allows:

```python
VALIDATOR_COMMENTS = Validator(
    allowed_tags={'b', 'i', 'strong', 'em', 'code', 'p', 'br', 'a'},
    allowed_attrs={'a': {'href', 'title'}},
    toolbar=['bold', 'italic', 'code', '|', 'link'],
    name='comments',
)
```

## Validator fields reference

| Field | Type | Default | Description |
|---|---|---|---|
| `allowed_tags` | `set[str]` | (required) | HTML tags that survive sanitization |
| `allowed_attrs` | `dict[str, set[str]]` | (required) | Allowed attributes per tag. `'*'` applies to all tags. |
| `filter_style_properties` | `set[str] \| None` | `None` | CSS properties allowed in `style` attributes |
| `generic_attribute_prefixes` | `set[str] \| None` | `None` | Attribute prefixes allowed on all tags (e.g. `{'data-'}`) |
| `url_schemes` | `set[str]` | `MARKDOWN_URL_SCHEMES` | Allowed URL schemes. Defaults to `{'http', 'https', 'mailto'}`. |
| `sanitize` | `bool` | `True` | Set to `False` to skip nh3 sanitization entirely |
| `name` | `str` | `'custom'` | Registration name for lookup by template filter and preview endpoint |
| `toolbar` | `list[str]` | `TOOLBAR_FULL` | EasyMDE toolbar buttons |
