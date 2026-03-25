from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .rendering import render_markdown
from .validators import VALIDATORS


@require_POST
@staff_member_required
def markdown_preview(request):
    text = request.POST.get('text', '')

    if len(text) > 102400:
        return JsonResponse({'error': 'Content too large'}, status=400)

    validator_name = request.POST.get('validator', 'standard')
    validator = VALIDATORS.get(validator_name)
    if validator is None:
        return JsonResponse({'error': 'Unknown validator'}, status=400)

    return JsonResponse({'html': render_markdown(text, validator)})
