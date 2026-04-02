# Backends

django-markdownfield uses a swappable backend for Markdown rendering. The backend converts Markdown
source text to raw HTML. Sanitization (nh3) and link processing happen after the backend, regardless
of which one is used.

```
source text -> backend() -> nh3.clean() -> process_links() -> safe HTML
```

Set `MARKDOWNFIELD_BACKEND` to select a backend. If not set, defaults to
`markdownfield.backends.markdownit`.

## Built-in backends

### markdown-it-py

Uses [markdown-it-py](https://github.com/executablebooks/markdown-it-py), a CommonMark 0.31.2
compliant renderer.

```python
MARKDOWNFIELD_BACKEND = 'markdownfield.backends.markdownit'
```

**HTML passthrough:** Raw HTML in Markdown source is passed through to the sanitizer by default. To
disable this (raw HTML is shown as literal text instead), set `MARKDOWNFIELD_ALLOW_HTML = False`.

**Plugins:** The markdown-it-py backend supports plugins via the `MARKDOWNFIELD_PLUGINS` setting.
Each entry is a dotted path to a function that takes a `MarkdownIt` instance and modifies it in
place:

```python
MARKDOWNFIELD_PLUGINS = [
    'mdit_py_plugins.tasklists.tasklists_plugin',
    'mdit_py_plugins.footnote.footnote_plugin',
]
```

Plugins are applied when the backend module is loaded. A collection of common plugins
(task lists, footnotes, containers, and more) is available in
[mdit-py-plugins](https://mdit-py-plugins.readthedocs.io/en/latest/), which is included as a
dependency.

### python-markdown

Uses [python-markdown](https://python-markdown.github.io/). For users migrating from an older
version of django-markdownfield or who depend on python-markdown extensions.

```python
MARKDOWNFIELD_BACKEND = 'markdownfield.backends.pymarkdown'
```

This backend reads the `MARKDOWN_EXTENSIONS` and `MARKDOWN_EXTENSION_CONFIGS` settings:

```python
MARKDOWNFIELD_BACKEND = 'markdownfield.backends.pymarkdown'
MARKDOWN_EXTENSIONS = ['fenced_code', 'tables', 'toc']
MARKDOWN_EXTENSION_CONFIGS = {
    'toc': {'permalink': True},
}
```

`MARKDOWN_EXTENSIONS` defaults to `['fenced_code']` if not set. These settings have no effect on
other backends.

## Custom backends

A backend is any Python module that defines a `render(text)` function. It receives Markdown source
text and returns raw (unsanitized) HTML. Sanitization is handled by the rendering pipeline after the
backend runs.

Point `MARKDOWNFIELD_BACKEND` to the module's dotted path:

```python
# settings.py
MARKDOWNFIELD_BACKEND = 'myapp.markdown'
```

```python
# myapp/markdown.py
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin

md = MarkdownIt('default', {'html': True})
footnote_plugin(md)

def render(text):
    return md.render(text)
```

If the module cannot be imported, an `ImportError` is raised. If it does not define a callable
`render`, a `TypeError` is raised.
