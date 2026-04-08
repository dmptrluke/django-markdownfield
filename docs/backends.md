# Backends

django-markdownfield uses a swappable backend for Markdown rendering. The backend converts Markdown
source text to raw HTML. Sanitization (nh3) and link processing happen outside of the backend.
```
source text -> backend() -> nh3.clean() -> process_links() -> safe HTML
```

Set `MARKDOWNFIELD_BACKEND` to select a backend. If not set, defaults to
`markdownfield.backends.markdownit`.

## Built-in backends

### markdown-it-py

The default backend since 0.18.0. Uses [markdown-it-py](https://github.com/executablebooks/markdown-it-py), a Python port of the
Javascript markdown-it project. This is a high-speed [CommonMark](https://commonmark.org/) compliant Markdown parser.

```python
MARKDOWNFIELD_BACKEND = 'markdownfield.backends.markdownit'
```

**Settings:**

| Setting | Default | Description |
|---|---|---|
| `MARKDOWNFIELD_ALLOW_HTML` | `True` | Pass raw HTML through to the sanitizer. When `False`, raw HTML is shown as literal text. |
| `MARKDOWNFIELD_LINKIFY` | `False` | Auto-link bare URLs (e.g. `https://example.com` becomes a clickable link without markdown syntax). |
| `MARKDOWNFIELD_TYPOGRAPHER` | `False` | Enable typographic replacements: smart quotes, (c)/(tm)/(r) symbols, em/en dashes. |
| `MARKDOWNFIELD_BREAKS` | `False` | Convert newlines in source to `<br>` tags. Without this, a single newline is ignored (standard CommonMark behavior). |

**Plugins:** 

The markdown-it-py backend supports plugins via the `MARKDOWNFIELD_PLUGINS` setting.
Each entry is a dotted path to a function that takes a `MarkdownIt` instance and modifies it in
place:

```python
MARKDOWNFIELD_PLUGINS = [
    'mdit_py_plugins.tasklists.tasklists_plugin',
    'mdit_py_plugins.footnote.footnote_plugin',
]
```

A collection of common plugins(task lists, footnotes, containers, and more) is available in
[mdit-py-plugins](https://mdit-py-plugins.readthedocs.io/en/latest/), which is included as a
dependency.

### python-markdown

The default (and only) backend before 0.18.0. Uses [python-markdown](https://python-markdown.github.io/). 
An older parser complaint with the original Markdown specification.

Useful for users migrating from older versions of django-markdownfield or who depend on
python-markdown extensions. To use this backend, an additional package needs to be installed:

```console
pip install django-markdownfield[pymarkdown]
```

```python
MARKDOWNFIELD_BACKEND = 'markdownfield.backends.pymarkdown'
```

**Extensions:** 

This backend reads the `MARKDOWN_EXTENSIONS` and `MARKDOWN_EXTENSION_CONFIGS` settings:

```python
MARKDOWNFIELD_BACKEND = 'markdownfield.backends.pymarkdown'
MARKDOWN_EXTENSIONS = ['fenced_code', 'tables', 'toc']
MARKDOWN_EXTENSION_CONFIGS = {
    'toc': {'permalink': True},
}
```

`MARKDOWN_EXTENSIONS` defaults to `['fenced_code']` if not set. 

Python Markdown includes a number of [official extenstions](https://python-markdown.github.io/extensions/).
More can be found in the [pymdownx](https://facelessuser.github.io/pymdown-extensions/) project.

## Custom backends

A backend is any Python module that defines a `render(text)` function. It receives Markdown source
text and returns raw (unsanitized) HTML. 

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
