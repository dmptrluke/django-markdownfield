# Changelog

## 0.20.0

### Changed

- Toolbar updated: three heading buttons replaced with a single cycling button (H1/H2/H3/H4), horizontal rule and guide removed, buttons regrouped into inline formatting, block (ish) formatting, lists, and insertions.
- Code block background styling scoped to inline code only. Fenced code blocks and raw HTML blocks no longer get the grey background.
- Fenced code block detection simplified to use parser state instead of mode sniffing, fixing false positives on raw HTML blocks.
- Tilde fences (`~~~`) disabled in the editor to prevent strikethrough (`~~`) from accidentally opening a code block.
- Horizontal rule syntax dimmed in the editor to match list markers.

## 0.19.0

### Changed

- Consolidated widget JS into a single `markdownfield.js` with no inline scripts. Editors auto-initialize via data attributes.
- Switched to a [custom EasyMDE build](https://github.com/dmptrluke/easymde-markdownfield) with marked, spell checker, and FA CDN downloads stripped out (-60KB).
- Font Awesome replaced with a 19-icon woff2 subset (2.7KB, down from 1MB).
- Static assets reduced from 1.38MB to 342KB.

### Added

- Table editing via [mte-kernel](https://github.com/susisu/mte-kernel): Tab/Shift-Tab to navigate cells, Enter for next row, Ctrl-Shift-F to format.
- Improved editor syntax styling: monospace code blocks and tables, dimmed list markers and table cell content.
- Third-party license files for bundled dependencies (EasyMDE, mte-kernel, Font Awesome).
- Support for optional CodeMirror language syntax highlighting in fenced code blocks (modes not shipped, but `window.CodeMirror` is exposed
  for users who want to add them).

## 0.18.4

### Fixed

- Include `markdown` (python-markdown) in test dependencies so pymarkdown backend tests pass in CI.

## 0.18.3

### Fixed

- Frontend editor toolbar buttons no longer show a border on hover.
- Added 1px margin between toolbar buttons.

## 0.18.2

### Changed

- `markdown` (python-markdown) moved to an optional dependency. Install with `pip install django-markdownfield[pymarkdown]`.

## 0.18.1

### Added

- `MARKDOWNFIELD_LINKIFY` to auto-link bare URLs.
- `MARKDOWNFIELD_TYPOGRAPHER` for smart quotes and typographic symbol replacements.
- `MARKDOWNFIELD_BREAKS` to convert newlines to `<br>` tags.

### Dependencies

- Added `linkify-it-py>=2.0`.

## 0.18.0

_If upgrading from 0.17.x or earlier: the default rendering backend has changed from python-markdown to markdown-it-py. Run `rerender_markdown` after upgrading. See breaking changes below._

### Changed

- **Breaking:** Default rendering backend switched to [markdown-it-py](https://github.com/executablebooks/markdown-it-py) (CommonMark 0.31.2). Rendered HTML may differ from python-markdown output. Run `rerender_markdown` after upgrading.
- **Breaking:** Link processing settings renamed to `MARKDOWNFIELD_` prefix. Old names still work as fallbacks.
  - `SITE_URL` -> `MARKDOWNFIELD_INTERNAL_URL` (now accepts a string or list)
  - `MARKDOWN_LINK_BLACKLIST` -> `MARKDOWNFIELD_BLOCKED_LINK_DOMAINS`
  - `MARKDOWN_MARK_EXTERNAL_LINKS` -> `MARKDOWNFIELD_MARK_EXTERNAL_LINKS`
- **Breaking:** URL schemes restricted to `http`, `https`, and `mailto` by default (`MARKDOWN_URL_SCHEMES`). Previous versions used nh3's broader default set (24 schemes including `ssh`, `irc`, `magnet`, `sms`, etc.). Custom validators can widen this via the `url_schemes` field.
- Table and strikethrough tags added to `MARKDOWN_TAGS` and buttons to `TOOLBAR_FULL`.
- Added `style="text-align:..."` support on `<th>` and `<td>` for table column alignment.
- `<iframe>`, `<script>`, and `<style>` tags now have their inner content stripped (not just the tag). Prevents content inside these tags from leaking into visible output.

### Added

- Swappable rendering backend via `MARKDOWNFIELD_BACKEND`. A python-markdown backend is included (`markdownfield.backends.pymarkdown`).
- `MARKDOWNFIELD_PLUGINS` for loading markdown-it-py plugins.
- `MARKDOWNFIELD_ALLOW_HTML` to disable raw HTML passthrough in the markdown-it-py backend.

### Dependencies

- Added `markdown-it-py>=4.0` and `mdit-py-plugins>=0.5.0`.

## 0.17.3 (2026-03-31)

- Bump pygments dependency (security update)

## 0.17.2 (2026-03-31)

- Improve PyPI metadata: add project URLs (Issues, Changelog), keywords, and SPDX license format
- Enable digital attestations in the release workflow

## 0.17.1 (2026-03-29)

### Fixed

- Fixed `MDEAdminWidget` being used for all forms instead of only admin views. Non-admin forms now correctly get the plain `MDEWidget`.

## 0.17.0 (2026-03-28)

### Added

- Added dark mode support for unfold-admin and other Tailwind-based admin themes using the `.dark` class convention. Editor, toolbar, preview, and all sub-elements themed using unfold's OKLCH palette tokens.

### Changed

- Editor widget CSS variables now chain through unfold's `--color-base-*` / `--color-font-*` / `--color-primary-*` tokens before falling back to hardcoded values. Stock Django admin is unaffected (its variables resolve first).
- Removed top border on CodeMirror editor to sit flush against the toolbar.

## 0.16.0 (2026-03-26)

### Added

- Added test suite (70 tests) covering rendering, validators, fields, link processing, preview endpoint, forms, template filter, system checks, and management command.

### Fixed

- Fixed `render_markdown` template filter output being auto-escaped in templates. `{{ text|render_markdown }}` now renders HTML correctly instead of showing raw tags.
- Fixed `MarkdownField.formfield()` returning a plain `Textarea` instead of `MDEWidget` when `use_editor=True`. Frontend ModelForms now get the EasyMDE editor widget.
- Fixed `MARKDOWN_EXTENSIONS`, `MARKDOWN_EXTENSION_CONFIGS`, `MARKDOWN_LINK_BLACKLIST`, and `MARKDOWN_MARK_EXTERNAL_LINKS` settings being read at import time. Runtime changes via Django settings (e.g. `override_settings` in tests) now take effect.

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
