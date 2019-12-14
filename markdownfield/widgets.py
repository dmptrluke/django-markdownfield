from django.forms import widgets


class EasyMDEEditor(widgets.Textarea):
    template_name = 'md_textfield.html'

    class Media:
        js = (
            'easymde.min.js',
        )

        css = {
            'all': (
                'easymde.min.css',
            )
        }
