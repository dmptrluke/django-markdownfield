from django.forms import widgets


class MDEWidget(widgets.Textarea):
    template_name = 'markdownfield/widget.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'data-easymde'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        js = (
            'markdownfield/easymde/easymde.min.js',
        )

        css = {
            'all': (
                'markdownfield/easymde/easymde.min.css',
                'markdownfield/fontawesome/font-awesome.min.css',
                'markdownfield/md.css',
            )
        }


class MDEAdminWidget(MDEWidget):
    template_name = 'markdownfield/widget.html'

    class Media:
        css = {
            'all': (
                'markdownfield/md_admin.css',
            )
        }
