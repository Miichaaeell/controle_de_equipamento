from ..models import Reason
import pytest


@pytest.mark.django_db
def test_reason_return():
    response, _ = Reason.objects.get_or_create(reason='Trocado')
    assert response.__str__() == 'Trocado'
