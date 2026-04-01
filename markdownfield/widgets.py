from django.forms import widgets
from django.urls.exceptions import NoReverseMatch

import shortuuid

from .validators import VALIDATORS


class MDEWidget(widgets.Textarea):
    template_name = 'markdownfield/widget.html'
    _utility_buttons = ['fullscreen', '|', 'guide']

    def __init__(self, options=None, validator_name='standard', **kwargs):
        super().__init__(**kwargs)
        self.uuid = shortuuid.uuid()
        self.validator_name = validator_name

        if options is None:
            options = {}

        self.options = options
        self.options_id = 'options_' + self.uuid

    def get_context(self, *args):
        context = super().get_context(*args)
        content = VALIDATORS[self.validator_name].toolbar
        context.update(
            {
                'options': self.options,
                'options_id': self.options_id,
                'toolbar': [*content, '|', *self._utility_buttons],
                'toolbar_id': 'toolbar_' + self.uuid,
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
    _utility_buttons = ['preview', 'fullscreen', '|', 'guide']

    def __init__(self, options=None, validator_name='standard', preview_url=None, **kwargs):
        super().__init__(options=options, validator_name=validator_name, **kwargs)
        self._preview_url = preview_url

    def get_context(self, *args):
        context = super().get_context(*args)

        preview_url = self._preview_url
        if preview_url is None:
            try:
                from django.urls import reverse

                preview_url = reverse('markdownfield:preview')
            except NoReverseMatch:
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
