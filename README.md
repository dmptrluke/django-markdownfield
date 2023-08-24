# django-markdownfield  [![PyPI](https://img.shields.io/pypi/v/django-markdownfield)](https://pypi.org/project/django-markdownfield/)
A simple custom field for Django that can safely render Markdown and store it in the database.

Your text is stored in a `MarkdownField`. When the model is saved, django-markdownfield will
parse the Markdown, render it, sanitise it with [bleach](https://github.com/mozilla/bleach), and store
the result in a `RenderedMarkdownField` for display to end users.

django-markdownfield also bundles a minified version of the [EasyMDE](https://github.com/Ionaru/easy-markdown-editor)
editor (v2.14.0) in admin views to make working with Markdown easier.

![alt test](https://raw.githubusercontent.com/dmptrluke/django-markdownfield/master/screenshots/editor.png)

## Installation

django-markdownfield can be installed from PyPi:

```console
# Install directly or add to your requirements.txt
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

## Usage

Implementing django-markdownfield is simple. See the below example.

First add `django-markdownfield` to your requirements or install simply with pip.
Then add `'markdownfield',` to your INSTALLED_APPS.


```python
from django.db import models

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

class Page(models.Model):
    text = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD)
    text_rendered = RenderedMarkdownField()
```

Please also set `SITE_URL` in your Django configuration - it will be needed for detecting
external links.

```python
SITE_URL = "https://example.com"
```

To disable the EasyMDE editor, see the amended line below.

```python
text = MarkdownField(rendered_field='text_rendered', use_editor=False, use_admin_editor=True)
```

### Use in templates

To use the rendered markdown in templates, just use the `RenderedMarkdownField()` you created on
your model, like below. This field should be marked as safe with the `safe` filter to ensure it
displays correctly.

```djangotemplate
{{ post.text_rendered | safe }}
```

## Validators
django-markdownfield comes with a number of validators, which are used to process and clean
the output of the markdown engine

### VALIDATOR_STANDARD
```python
from markdownfield.validators import VALIDATOR_STANDARD
```
This validator strips any tags that are not used by standard Markdown. It also automatically links
any URLs in the output, adding `class="external"`, `rel="nofollow noopener noreferrer"`, and
`target="_blank"` to any URLs which it determines to be external.

### VALIDATOR_CLASSY
```python
from markdownfield.validators import VALIDATOR_CLASSY
```
This validator does much the same as `VALIDATOR_STANDARD`, but it allows you to set the class on
links and images. This is useful to create buttons and other enhanced links.

### VALIDATOR_NULL
```python
from markdownfield.validators import VALIDATOR_NULL
```
This validator does not call [bleach](https://github.com/mozilla/bleach) to sanitize the output at all.
This is **not safe for user input**.  It allows arbitrary (unsafe) HTML in your markdown input.


### Creating Custom Validators
To create a custom validator, just create an instance of  the `markdownfield.validators.Validator`
dataclass. An example of this is shown below.

```python
from markdownfield.validators import Validator

# allows only bold and italic text
VALIDATOR_COMMENTS = Validator(
    allowed_tags=["b", "i", "strong", "em"],
    allowed_attrs={},
    linkify=False
)
```

You can also find a standard set of markdown-safe tags and attrs in `markdownfield.validators`, and extend
that.

```python
from markdownfield.validators import Validator, MARKDOWN_TAGS, MARKDOWN_ATTRS

# allows all standard markdown features,
# but also allows the class to be set on images and links
VALIDATOR_CLASSY = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        'img': ['src', 'alt', 'title', 'class'],
        'a': ['href', 'alt', 'title', 'name', 'class']
    }
)
```

## Migrations

If you need to migrate from TextField or CharField to the MarkdownField you need to migrate the stored `text` also in the `rendered_text` field.
Update your auto-created migration fiele and add the method below. 
Use a method to `save()` every instance of your model once after the migrations, so the text will be copied into the `text_rendered` field correctly.

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
Copyright (c) 2019-2021 Luke Rogers

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
