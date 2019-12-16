from django.forms import widgets


class MDEditor(widgets.Textarea):
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


class AdminMDEditor(MDEditor):
    class Media:
        css = {
            'all': (
                'md_admin.css',
            )
        }
