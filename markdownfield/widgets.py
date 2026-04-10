from django.forms import widgets
from django.urls.exceptions import NoReverseMatch

import shortuuid

from .validators import VALIDATORS


class MDEWidget(widgets.Textarea):
    template_name = 'markdownfield/widget.html'
    _utility_buttons = ['fullscreen']

    def __init__(self, options=None, validator_name='standard', **kwargs):
        super().__init__(**kwargs)
        self.uuid = shortuuid.uuid()
        self.validator_name = validator_name
        self.options = options if options is not None else {}
        self.config_id = 'mdf_cfg_' + self.uuid

    def get_context(self, *args):
        context = super().get_context(*args)
        toolbar = VALIDATORS[self.validator_name].toolbar
        context['widget']['attrs']['data-markdownfield'] = self.config_id
        context.update(
            {
                'config': {
                    'toolbar': [*toolbar, '|', *self._utility_buttons],
                    'options': self.options,
                },
                'config_id': self.config_id,
            }
        )
        return context

    class Media:
        js = (
            'markdownfield/easymde/easymde.min.js',
            'markdownfield/markdownfield.js',
            'markdownfield/mte/mte-kernel.min.js',
            'markdownfield/mte/mte-plugin.js',
        )

        css = {
            'all': (
                'markdownfield/easymde/easymde.min.css',
                'markdownfield/md.css',
                'markdownfield/md_frontend.css',
            )
        }


class MDEAdminWidget(MDEWidget):
    _utility_buttons = ['fullscreen']

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

        if preview_url:
            context['config']['preview'] = {
                'url': preview_url,
                'validator': self.validator_name,
            }

        return context

    class Media:
        extend = False
        js = (
            'markdownfield/easymde/easymde.min.js',
            'markdownfield/markdownfield.js',
            'markdownfield/mte/mte-kernel.min.js',
            'markdownfield/mte/mte-plugin.js',
        )
        css = {
            'all': (
                'markdownfield/easymde/easymde.min.css',
                'markdownfield/md.css',
                'markdownfield/md_admin.css',
            )
        }
