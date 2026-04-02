from io import StringIO

from django.core.management import call_command

import pytest

from .models import SamplePost

pytestmark = pytest.mark.django_db


class TestRerenderMarkdown:
    # command re-renders all instances
    def test_rerender_updates_all_instances(self, db):
        post = SamplePost.objects.create(body='**bold**')
        # manually corrupt the rendered field
        SamplePost.objects.filter(pk=post.pk).update(body_rendered='stale')
        post.refresh_from_db()
        assert post.body_rendered == 'stale'

        call_command('rerender_markdown', stdout=StringIO())

        post.refresh_from_db()
        assert '<strong>bold</strong>' in post.body_rendered

    # --dry-run reports changes without writing to the database
    def test_dry_run_does_not_write(self, db):
        post = SamplePost.objects.create(body='**bold**')
        SamplePost.objects.filter(pk=post.pk).update(body_rendered='stale')

        call_command('rerender_markdown', dry_run=True, stdout=StringIO())

        post.refresh_from_db()
        assert post.body_rendered == 'stale'

    # no error when the model has zero rows
    def test_handles_empty_table(self, db):
        stdout = StringIO()
        call_command('rerender_markdown', stdout=stdout)
        assert '0 rows' in stdout.getvalue()
