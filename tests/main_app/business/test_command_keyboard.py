from base_site.mainapp.business.valid_commands import get_valid_commands
from base_site.mainapp.command_keyboard import CommandKeyBoard
from base_site.mainapp.models import Category
from base_site.mainapp.models import FullCommand
from django.test import TestCase


class CommandKeyBoardTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Cat1")
        Category.objects.create(name="ACat1")
        Category.objects.create(name="BCat1")

    def test_should_get_category_return_categories_on_alphabetical_order(self):

        result = CommandKeyBoard.get_category()
        self.assertEqual(result[0][0][0].text, "ACat1")
        self.assertEqual(result[0][0][1].text, "BCat1")
        self.assertEqual(result[0][0][2].text, "Cat1")

    def test_should_not_return_enable_false_categories(self):
        Category.objects.create(name="Block", enable=False)

        result = CommandKeyBoard.get_category()
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(len(result[0][0]), 3)
