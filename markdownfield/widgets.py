from django.forms import widgets

import shortuuid


class MDEWidget(widgets.Textarea):
    template_name = 'markdownfield/widget.html'

    def __init__(self, options=None, **kwargs):
        super().__init__(**kwargs)
        self.uuid = shortuuid.uuid()

        if options is None:
            options = {}

        self.options = options
        self.options_id = 'options_' + self.uuid

    def get_context(self, *args):
        context = super().get_context(*args)
        context.update({
            'options': self.options,
            'options_id': self.options_id,
        })
        return context

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
