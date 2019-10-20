from base_site.mainapp.business.valid_commands import get_valid_commands
from base_site.mainapp.models import FullCommand
from django.test import TestCase


class ModelExampleTestCase(TestCase):
    def setUp(self):
        FullCommand.objects.create(command="/a", entry_date=False, payment_date=3)
        FullCommand.objects.create(command="/test", entry_date=False, payment_date=3)

    def test_get_valid_commands(self):

        expected_list = ["a", "test"]
        self.assertListEqual(expected_list, get_valid_commands())
