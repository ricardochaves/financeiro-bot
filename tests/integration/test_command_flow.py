from base_site.mainapp.business.command_flow import CommandFlow
from django.core.management import call_command
from django.test import TestCase


class ModelExampleTestCase(TestCase):
    def setUp(self):
        call_command("seeddb")

    def test_command_no_credit(self):

        command = CommandFlow("/a")

        self.assertEqual(command.next("/a")["message"], "Informe o valor de débito")
        self.assertEqual(command.next("100")["message"], "Informe o valor de crédito")
        self.assertEqual(command.next("10")["message"], "Informe a descrição")
        self.assertEqual(command.next("description")["message"], "Informe a data de lançamento")
        self.assertEqual(command.next("21-06-1981")["message"], "Informe a data de pagamento")
        self.assertEqual(command.next("21-06-1981")["message"], "Informe a categoria")
        self.assertEqual(command.next("21-06-1981")["message"], "Informe o nome")
        self.assertEqual(command.next("Name")["message"], "Informe o tipo")
        self.assertTrue(command.next("Variável")["done"])

    def test_command_credit(self):

        command = CommandFlow("/ac")

        self.assertEqual(command.next("/ac")["message"], "Informe o valor de débito")
        self.assertEqual(command.next("100")["message"], "Informe o valor de crédito")
        self.assertEqual(command.next("10")["message"], "Informe a descrição")
        self.assertEqual(command.next("description")["message"], "Informe a data de lançamento")
        self.assertEqual(command.next("21-06-1981")["message"], "Informe a categoria")
        self.assertEqual(command.next("21-06-1981")["message"], "Informe o nome")
        self.assertEqual(command.next("Name")["message"], "Informe o tipo")
        self.assertEqual(command.next("type1")["message"], "Informe o número de parcelas")
        self.assertTrue(command.next("Variável")["done"])
