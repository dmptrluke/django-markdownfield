import pytest

pytestmark = pytest.mark.django_db

URL = '/markdownfield/preview/'


class TestPreviewEndpoint:
    # unauthenticated request is rejected
    def test_anonymous_user_rejected(self, client):
        response = client.post(URL, {'text': '**bold**'})
        assert response.status_code == 302

    # non-staff user is rejected
    def test_non_staff_rejected(self, client, regular_user):
        client.login(username='regular', password='password')
        response = client.post(URL, {'text': '**bold**'})
        assert response.status_code == 302

    # GET method returns 405
    def test_get_method_rejected(self, staff_client):
        response = staff_client.get(URL)
        assert response.status_code == 405

    # staff user can preview markdown
    def test_staff_can_preview(self, staff_client):
        response = staff_client.post(URL, {'text': '**bold**'})
        assert response.status_code == 200
        data = response.json()
        assert '<strong>bold</strong>' in data['html']

    # validator parameter selects the correct validator
    def test_validator_parameter_respected(self, staff_client):
        response = staff_client.post(URL, {'text': '# Heading', 'validator': 'basic'})
        data = response.json()
        assert '<h1>' not in data['html']

    # unknown validator name returns 400
    def test_unknown_validator_returns_error(self, staff_client):
        response = staff_client.post(URL, {'text': 'test', 'validator': 'nonexistent'})
        assert response.status_code == 400
        assert 'error' in response.json()

    # input exceeding 102400 bytes returns 400
    def test_oversized_input_rejected(self, staff_client):
        response = staff_client.post(URL, {'text': 'x' * 102401})
        assert response.status_code == 400

    # empty input renders to empty string
    def test_empty_input_returns_empty(self, staff_client):
        response = staff_client.post(URL, {'text': ''})
        assert response.status_code == 200
        assert response.json()['html'] == ''
