from api.models import Customer, Meter, MeterType
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestModels:

    def test_customer_count(self, django_db_setup):
        assert Customer.objects.count() > 0

    def test_meter_count(self, django_db_setup):
        assert Meter.objects.count() > 0

    def test_meter_type(self, django_db_setup):
        assert MeterType.objects.count() > 0
