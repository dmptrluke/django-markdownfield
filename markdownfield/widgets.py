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
        context.update(
            {
                'options': self.options,
                'options_id': self.options_id,
            }
        )
        return context

    class Media:
        js = ('markdownfield/easymde/easymde.min.js',)

        css = {
            'all': (
                'markdownfield/easymde/easymde.min.css',
                'markdownfield/fontawesome/font-awesome.min.css',
                'markdownfield/md.css',
            )
        }


class MDEAdminWidget(MDEWidget):
    template_name = 'markdownfield/admin_widget.html'

    def __init__(self, options=None, validator_name='standard', preview_url=None, **kwargs):
        super().__init__(options=options, **kwargs)
        self.validator_name = validator_name
        self._preview_url = preview_url

    def get_context(self, *args):
        context = super().get_context(*args)

        preview_url = self._preview_url
        if preview_url is None:
            try:
                from django.urls import reverse

                preview_url = reverse('markdownfield:preview')
            except Exception:
                preview_url = None

        context['validator_name'] = self.validator_name
        context['preview_url'] = preview_url
        return context

    class Media:
        extend = False
        js = ('markdownfield/easymde/easymde.min.js',)
        css = {
            'all': (
                'markdownfield/easymde/easymde.min.css',
                'markdownfield/fontawesome/font-awesome.min.css',
                'markdownfield/md_admin.css',
            )
        }
