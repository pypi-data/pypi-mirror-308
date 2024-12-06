from django.test import TestCase
from django.urls import reverse

from dcim.models import Site, Location

from sop_infra.models import SopInfra


class SopInfraViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.minas = Site.objects.create(
            name="Minas Tirith",
            slug="minas-tirith",
            status="active"
        )
        cls.bree = Site.objects.create(
            name="Bree",
            slug="bree",
            status="candidate"
        )
        cls.gondor = Location.objects.create(
            name="Gondor",
            slug="gondor",
            site=cls.minas
        )

    def test_sopinfra_view(self):
        infra = SopInfra.objects.create(
            site=self.bree
        )
        infra.full_clean()
        infra.save()
        url = reverse('plugins:sop_infra:sopinfra_detail', args=[infra.pk])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)


