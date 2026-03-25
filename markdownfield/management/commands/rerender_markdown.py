from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import DatabaseError

from ...models import MarkdownField
from ...rendering import render_markdown


class Command(BaseCommand):
    help = 'Re-render all MarkdownField values into their corresponding RenderedMarkdownFields.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report what would change without writing to the database.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        for model in apps.get_models():
            for field in model._meta.get_fields():
                if not isinstance(field, MarkdownField) or not field.rendered_field:
                    continue

                count = model.objects.count()
                self.stdout.write(f'Re-rendering {model.__name__}.{field.name}: {count} rows')

                if dry_run:
                    continue

                batch = []
                for obj in model.objects.all().iterator(chunk_size=500):
                    source = getattr(obj, field.attname)
                    rendered = render_markdown(source, field.validator)
                    setattr(obj, field.rendered_field, rendered)
                    batch.append(obj)

                    if len(batch) >= 500:
                        try:
                            model.objects.bulk_update(batch, [field.rendered_field], batch_size=500)
                        except DatabaseError as e:
                            self.stderr.write(f'Error updating {model.__name__}: {e}')
                        batch = []

                if batch:
                    try:
                        model.objects.bulk_update(batch, [field.rendered_field], batch_size=500)
                    except DatabaseError as e:
                        self.stderr.write(f'Error updating {model.__name__}: {e}')
