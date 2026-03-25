# django-markdownfield  [![PyPI](https://img.shields.io/pypi/v/django-markdownfield)](https://pypi.org/project/django-markdownfield/)
A simple custom field for Django that can safely render Markdown and store it in the database.

Your text is stored in a `MarkdownField`. When the model is saved, django-markdownfield will
parse the Markdown, render it, sanitise it with [nh3](https://github.com/messense/nh3), and store
the result in a `RenderedMarkdownField` for display to end users.

django-markdownfield also bundles a minified version of the [EasyMDE](https://github.com/Ionaru/easy-markdown-editor)
editor (v2.20.0) for use in admin and frontend forms.

![Editor screenshot](https://raw.githubusercontent.com/dmptrluke/django-markdownfield/master/screenshots/editor.png)

## Installation

django-markdownfield can be installed from PyPI:

```console
pip install django-markdownfield
```

After installation, you need to add `markdownfield` to `INSTALLED_APPS` of your Django project's settings.

```python
INSTALLED_APPS = [
    "markdownfield",
    ...
    "django.contrib.staticfiles",
]
```

To enable the admin preview endpoint, add the URL configuration:

```python
urlpatterns = [
    path('markdownfield/', include('markdownfield.urls')),
    ...
]
```

## Usage

Add a `MarkdownField` and a paired `RenderedMarkdownField` to your model:

```python
from django.db import models

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

class Page(models.Model):
    text = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD)
    text_rendered = RenderedMarkdownField()
```

Whenever your model is saved, the `RenderedMarkdownField` will be updated automatically.

## Displaying content

To display the rendered markdown in your template, just display the `RenderedMarkdownField` like any other field.
```jinja
{{ post.text_rendered }}
```

### Using the template filter

If you don't want to use a `RenderedMarkdownField`, use the template filter to render Markdown in your templates directly:

```jinja
{% load markdownfield %}

{{ post.raw_text|render_markdown }}
{{ post.raw_text|render_markdown:"classy" }}
```

The argument is a validator name (`standard`, `classy`, `basic`, `null`). Defaults to `standard`.

### Using render_markdown() directly

```python
from markdownfield.rendering import render_markdown
from markdownfield.validators import VALIDATOR_STANDARD

html = render_markdown('**bold**', VALIDATOR_STANDARD)
```

## Editor

The bundled EasyMDE editor is available in both admin and frontend forms.

### Admin

The EasyMDE editor is enabled automatically in the Django admin. To disable it:

```python
text = MarkdownField(rendered_field='text_rendered', use_admin_editor=False)
```

### Frontend forms

The editor widget is also included automatically in frontend `ModelForm`s. You must include the
form's media in your template or the editor's JavaScript and CSS will not load:

```jinja
<head>
    {{ form.media.css }}
</head>
<body>
    <form method="post">
        {% csrf_token %}
        {{ form }}
        <button type="submit">Save</button>
    </form>
    {{ form.media.js }}
</body>
```

To disable the editor in frontend forms:

```python
text = MarkdownField(rendered_field='text_rendered', use_editor=False)
```

To customise the EasyMDE options, override the widget in your form. Any
[EasyMDE configuration option](https://github.com/Ionaru/easy-markdown-editor#options-list) can be
passed via the `options` dict:

```python
from django import forms
from markdownfield.widgets import MDEWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text': MDEWidget(options={'toolbar': ['bold', 'italic', 'link']}),
        }
```

## Configuration

All settings are optional.

| Setting | Default | Description |
|---|---|---|
| `SITE_URL` | `None` | Your site's base URL (e.g. `"https://example.com"`). Used to distinguish internal from external links. Without it, all links are treated as external. |
| `MARKDOWN_EXTENSIONS` | `['fenced_code']` | List of [Python-Markdown extensions](https://python-markdown.github.io/extensions/) to enable. |
| `MARKDOWN_EXTENSION_CONFIGS` | `{}` | Configuration for Markdown extensions. |
| `MARKDOWN_LINK_BLACKLIST` | `[]` | List of domains whose `<a>` links should be stripped from output (e.g. `['spam.example.com']`). The link text is preserved; only the link itself is removed. |
| `MARKDOWN_MARK_EXTERNAL_LINKS` | `True` | When `True`, external links receive `target="_blank"` and `class="external"`. Set to `False` to disable. |

## Validators

django-markdownfield comes with a number of validators, which are used to process and clean the output of the Markdown engine.

### VALIDATOR_STANDARD
```python
from markdownfield.validators import VALIDATOR_STANDARD
```
This validator strips any tags not used by standard Markdown.

### VALIDATOR_CLASSY
```python
from markdownfield.validators import VALIDATOR_CLASSY
```
Like `VALIDATOR_STANDARD`, but also allows `class` on links and images, and permits `data-*`
attributes. Useful for creating styled buttons and enhanced links.

### VALIDATOR_BASIC
```python
from markdownfield.validators import VALIDATOR_BASIC
```
Allows only inline formatting: bold, italic, strikethrough, inline code, and links.

### VALIDATOR_NULL
```python
from markdownfield.validators import VALIDATOR_NULL
```
Skips sanitization entirely. **Not safe for user input.** Allows arbitrary HTML in Markdown input.


### Creating Custom Validators

To create a custom validator, create an instance of the `markdownfield.validators.Validator` dataclass:

```python
from markdownfield.validators import Validator

# allows only bold and italic text
VALIDATOR_COMMENTS = Validator(
    allowed_tags={'b', 'i', 'strong', 'em'},
    allowed_attrs={},
)
```

You can also extend the built-in tag and attribute sets:

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
)
```

To allow inline CSS but restrict which properties are permitted:

```python
VALIDATOR_STYLED = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        '*': {'id', 'style'},
    },
    filter_style_properties={'color', 'font-weight', 'text-align'},
)
```

Note: `filter_style_properties` has no effect unless `style` is included in `allowed_attrs`. If `style` is allowed but `filter_style_properties` is not set, all CSS properties are permitted.

To restrict permitted URL schemes (e.g. block `javascript:` or custom schemes):

```python
VALIDATOR_STRICT = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs=MARKDOWN_ATTRS,
    url_schemes={'http', 'https', 'mailto'},
)
```

## Management commands

### rerender_markdown

Re-renders all `MarkdownField` values into their paired `RenderedMarkdownField`s. Useful after changing validators, markdown extensions, or upgrading django-markdownfield.

```console
python manage.py rerender_markdown
python manage.py rerender_markdown --dry-run
```

## Migrations

If you need to migrate from `TextField` or `CharField` to `MarkdownField`, add a `RunPython` step to your migration that calls `save()` on every existing instance so the rendered field is populated:

```python
from django.db import migrations
import markdownfield.models


def save_text_rendered(apps, schema_editor):
    ExampleModel = apps.get_model('yourapp', 'ExampleModel')
    for examplemodel in ExampleModel.objects.all():
        examplemodel.save()


class Migration(migrations.Migration):

    dependencies = [
        ('yourapp', '000X_migrate_to_markdownfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='yourapp',
            name='text_rendered',
            field=markdownfield.models.RenderedMarkdownField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ExampleModel',
            name='text',
            field=markdownfield.models.MarkdownField(rendered_field='text_rendered'),
        ),
        migrations.RunPython(save_text_rendered),
    ]
```

## License

This software is released under the MIT license.
```
Copyright (c) 2019-2026 Luke Rogers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
