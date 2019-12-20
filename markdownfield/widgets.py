from django.forms import widgets


class MDEWidget(widgets.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'data-easymde'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        js = (
            'markdownfield/easymde/easymde.min.js',
            'markdownfield/md.js',
        )

        css = {
            'all': (
                'markdownfield/easymde/easymde.min.css',
                'markdownfield/md.css',
            )
        }


class MDEAdminWidget(MDEWidget):
    class Media:
        css = {
            'all': (
                'markdownfield/md_admin.css',
            )
        }
