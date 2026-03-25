from django.contrib.auth.models import User

import pytest

from .models import SamplePost


@pytest.fixture
def post(db):
    return SamplePost.objects.create(body='**bold** text')


@pytest.fixture
def staff_user(db):
    return User.objects.create_user('staff', password='password', is_staff=True)


@pytest.fixture
def staff_client(client, staff_user):
    client.login(username='staff', password='password')
    return client


@pytest.fixture
def regular_user(db):
    return User.objects.create_user('regular', password='password')
