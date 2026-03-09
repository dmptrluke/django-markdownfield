# Changelog

## 0.12.1 (2026-03-09)

### Fixes

- Editor widget script now uses an IIFE, fixing a `SyntaxError` when the widget is used in Django formsets or admin inlines where field names contain hyphens (e.g. `form-0-body`). Also prevents variable collisions when multiple markdown fields appear on the same page. ([#13](https://github.com/dmptrluke/django-markdownfield/issues/13), [#38](https://github.com/dmptrluke/django-markdownfield/issues/38))

## 0.12.0 (2026-03-09)

### Breaking changes

**Replaced `bleach` with `nh3`** for HTML sanitization. `bleach` has been unmaintained since 2023; `nh3` is the actively maintained Rust-based replacement.

Custom validators must be updated. Before:

```python
from bleach.css_sanitizer import CSSSanitizer
from markdownfield.validators import Validator

MY_VALIDATOR = Validator(
    allowed_tags=['p', 'strong', 'em', 'a', 'img'],
    allowed_attrs={
        '*': ['id'],
        'img': ['src', 'alt', 'title'],
        'a': ['href', 'alt', 'title'],
    },
    css_sanitizer=CSSSanitizer(allowed_css_properties=['color', 'font-weight']),
)
```

After:

```python
from markdownfield.validators import Validator

MY_VALIDATOR = Validator(
    allowed_tags={'p', 'strong', 'em', 'a', 'img'},
    allowed_attrs={
        '*': {'id', 'style'},
        'img': {'src', 'alt', 'title'},
        'a': {'href', 'alt', 'title'},
    },
    filter_style_properties={'color', 'font-weight'},
)
```

**`Validator.linkify` removed and bare URL auto-linkification dropped.** `bleach`'s `LinkifyFilter` previously auto-linkified plain-text URLs and drove external link processing. Both are now handled differently: Markdown links (`[text](url)`) work as before; external link marking (`target="_blank"`, `class="external"`) always applies when `sanitize=True`. To restore bare URL auto-linkification, add `pymdownx.magiclink` to `MARKDOWN_EXTENSIONS`.

**`MARKDOWN_LINKIFY_BLACKLIST` renamed to `MARKDOWN_LINK_BLACKLIST`.** The setting now strips any `<a>` link pointing to a blacklisted domain (preserving the link text), rather than only suppressing auto-linkified URLs.

**Dropped Python 3.8 and 3.9 support** (both reached end-of-life).

### Changes

- Bundled EasyMDE updated from v2.14.0 to v2.20.0.
- `<script>` and `<style>` tags are now fully removed including their content (`clean_content_tags`), rather than just stripping the tag and leaving the text visible.
- External links now receive `rel="nofollow noopener noreferrer"` via nh3's native `link_rel` parameter.
- `Validator` now supports `url_schemes: set[str] | None` to restrict which URL schemes are permitted in `href`/`src` attributes (e.g. `{'http', 'https', 'mailto'}`). Defaults to `None` (nh3 built-in safe defaults).
- `Validator` now supports `generic_attribute_prefixes: set[str] | None` to allow wildcard attribute prefixes such as `data-`. `VALIDATOR_CLASSY` includes `{'data-'}` by default.
- New `MARKDOWN_MARK_EXTERNAL_LINKS` setting (default `True`) controls whether external links receive `target="_blank"` and `class="external"`.
- Migrated build backend from `flit` to `hatchling`.
- Migrated dependency management to `uv`.
- Switched linting and formatting from `flake8` + `isort` to `ruff`.

### Fixes

- CSP nonce in the editor widget is now conditional: supports `django-csp` (context processor `csp_nonce`), `django-csp-helpers` (`request.csp_nonce`), and no-CSP setups. ([#26](https://github.com/dmptrluke/django-markdownfield/issues/26))

## 0.11.0

Previous release.
