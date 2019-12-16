from django.forms import widgets


class MDEditor(widgets.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'data-easymde'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        js = (
            'easymde.min.js', 'md.js'
        )

        css = {
            'all': (
                'easymde.min.css',
            )
        }


class AdminMDEditor(MDEditor):
    class Media:
        css = {
            'all': (
                'md_admin.css',
            )
        }
