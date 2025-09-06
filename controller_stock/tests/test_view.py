import pytest

from django.urls import reverse
from ..models import Reason, Location


def test_controller_stock_view(admin_client):
    url = reverse('stock')
    response = admin_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_create_reason_view(admin_client):
    url = reverse('create_reason')
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_create_reason_view(admin_client):
    url = reverse('create_reason')
    response = admin_client.post(
        url,
        {
            'reason': 'teste'
        }

    )
    obj_created = Reason.objects.filter(reason='teste').first()
    assert response.status_code == 302
    assert obj_created is not None


@pytest.mark.django_db
def test_get_create_location_view(admin_client):
    url = reverse('create_location')
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_create_location_view(admin_client):
    url = reverse('create_location')
    response = admin_client.post(
        url,
        {
            'location': 'teste',
            'type': 'estoque',
            'user': ''
        }
    )
    obj_created = Location.objects.get(location='teste')
    assert response.status_code == 302
    assert obj_created is not None
