from django.test import TestCase
from ..models import Reason, Location


class ReasonTest(TestCase):
    def setUp(self):
        Reason.objects.create(reason='Trocado')

    def test_reason_return(self):
        response = Reason.objects.get(reason='Trocado')

        self.assertEqual(response.__str__(), 'Trocado')


class LocationTest(TestCase):
    def setUp(self):
        Location.objects.create(location='Estoque')

    def test_location_return(self):
        response = Location.objects.get(location__icontains='estoque')

        self.assertEqual(response.__str__(), 'Estoque')
