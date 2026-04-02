import importlib

from django.conf import settings
from django.test.signals import setting_changed

_backend = None

DEFAULT_BACKEND = 'markdownfield.backends.markdownit'


def get_backend():
    """Return the active markdown backend callable, cached per process."""
    global _backend
    if _backend is None:
        _backend = _resolve_backend()
    return _backend


def _resolve_backend():
    path = getattr(settings, 'MARKDOWNFIELD_BACKEND', DEFAULT_BACKEND)
    module = importlib.import_module(path)
    importlib.reload(module)
    render = getattr(module, 'render', None)
    if not callable(render):
        raise TypeError(f'MARKDOWNFIELD_BACKEND module {path!r} must define a callable render()')
    return render


def _clear_backend_cache(setting, **kwargs):
    global _backend
    _backend = None


setting_changed.connect(_clear_backend_cache)
