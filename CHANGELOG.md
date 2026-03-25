# Changelog

## 0.15.1 (2026-03-25)

### Fixed

- Fix build issue.

## 0.15.0 (2026-03-25)

### Added

- Extracted rendering pipeline into `render_markdown()` for standalone use without the dual-column pattern.
- Added `render_markdown` template filter via `{% load markdownfield %}`. ([#19](https://github.com/dmptrluke/django-markdownfield/issues/19))
- Added server-side preview endpoint and admin widget preview button. ([#10](https://github.com/dmptrluke/django-markdownfield/issues/10))
- Added `rerender_markdown` management command for bulk re-rendering all stored markdown.
- Added Django system checks for mismatched `rendered_field` references (W001) and missing URL configuration (W002).
- Added validator self-registration via `VALIDATORS` dict for name-based lookup.
- Added automatic `mark_safe()` on `RenderedMarkdownField` values loaded from the database.

### Fixed

- Fixed editor preview pane unreadable in Django admin dark mode - replaced hardcoded colors with admin CSS variables.
- Fixed heading spacing in editor preview - more space above, less below.

## 0.14.0 (2026-03-25)

### Changed

- Bump minimum Django version to 4.2.
- Add CI and release workflows, update Django classifiers.
- Update code blocks from `djangotemplate` to `jinja` language hint.

## 0.13.2 (2026-03-09)

### Fixed

- Disabled EasyMDE automatic Font Awesome CDN download to prevent unwanted external network requests.

## 0.13.1 (2026-03-09)

### Changed

- Restructured README editor documentation into Admin and Frontend sections, added frontend form media example and EasyMDE options example.

## 0.13.0 (2026-03-09)

### Added

- Added `VALIDATOR_BASIC` preset -- allows only inline formatting (`b`, `i`, `strong`, `em`, `del`, `code`, `a`, `p`, `br`), suitable for comments, bios, and short user-generated content.

### Changed

- Allowed `width` and `height` attributes on `<img>` in `VALIDATOR_STANDARD` and `VALIDATOR_CLASSY`.

### Fixed

- Wrapped editor widget script in an IIFE, fixing a `SyntaxError` when the widget is used in Django formsets or admin inlines where field names contain hyphens (e.g. `form-0-body`). Also prevents variable collisions when multiple markdown fields appear on the same page. ([#13](https://github.com/dmptrluke/django-markdownfield/issues/13), [#38](https://github.com/dmptrluke/django-markdownfield/issues/38))

## 0.12.0 (2026-03-09)

_If upgrading from 0.11.x: custom validators must be updated for nh3. See breaking changes below._

### Added

- Added `url_schemes` parameter to `Validator` for restricting which URL schemes are permitted in `href`/`src` attributes (e.g. `{'http', 'https', 'mailto'}`). Defaults to `None` (nh3 built-in safe defaults).
- Added `generic_attribute_prefixes` parameter to `Validator` for wildcard attribute prefixes such as `data-`. `VALIDATOR_CLASSY` includes `{'data-'}` by default.
- Added `MARKDOWN_MARK_EXTERNAL_LINKS` setting (default `True`) to control whether external links receive `target="_blank"` and `class="external"`.

### Changed

- **Breaking:** Replaced `bleach` with `nh3` for HTML sanitization. `bleach` has been unmaintained since 2023; `nh3` is the actively maintained Rust-based replacement. Custom validators must be updated:

  Before:

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

- **Breaking:** Removed `Validator.linkify` field and dropped bare URL auto-linkification. Markdown links (`[text](url)`) work as before; external link marking (`target="_blank"`, `class="external"`) always applies when `sanitize=True`. To restore bare URL auto-linkification, add `pymdownx.magiclink` to `MARKDOWN_EXTENSIONS`.
- **Breaking:** Renamed `MARKDOWN_LINKIFY_BLACKLIST` to `MARKDOWN_LINK_BLACKLIST`. The setting now strips any `<a>` link pointing to a blacklisted domain (preserving the link text), rather than only suppressing auto-linkified URLs.
- Updated bundled EasyMDE from v2.14.0 to v2.20.0. ([#27](https://github.com/dmptrluke/django-markdownfield/issues/27))
- Stripped `<script>` and `<style>` tags including their content (`clean_content_tags`), rather than just stripping the tag and leaving the text visible.
- Added `rel="nofollow noopener noreferrer"` to external links via nh3's native `link_rel` parameter.
- Migrated build backend from `flit` to `hatchling`.
- Migrated dependency management to `uv`.
- Switched linting and formatting from `flake8` + `isort` to `ruff`.

### Fixed

- Made CSP nonce in the editor widget conditional: supports `django-csp` (context processor `csp_nonce`), `django-csp-helpers` (`request.csp_nonce`), and no-CSP setups. ([#26](https://github.com/dmptrluke/django-markdownfield/issues/26))
- Restored flat toolbar button theming in Django admin. ([#37](https://github.com/dmptrluke/django-markdownfield/issues/37))
- Fixed field margin and fullscreen z-index in admin. ([#33](https://github.com/dmptrluke/django-markdownfield/issues/33))

### Removed

- **Breaking:** Dropped Python 3.8 and 3.9 support (both reached end-of-life).

## 0.11.0

Previous release.
