from base_site.mainapp.business.register import Register
from django.test import TestCase
from tests.helper import create_scenario_with_two_commands_complete_and_empty


class RegisterClassTestCase(TestCase):
    def setUp(self):
        self.category, self.family_member, self.type_entry, self.empty_command, self.completed_command = (
            create_scenario_with_two_commands_complete_and_empty()
        )

    def test_should_return_true_for_all_options(self):

        register = Register(self.empty_command)

        self.assertFalse(register.need_payment_installments())
        self.assertTrue(register.need_entry_date())
        self.assertTrue(register.need_payment_date())
        self.assertTrue(register.need_debit())
        self.assertTrue(register.need_credit())
        self.assertTrue(register.need_category())
        self.assertTrue(register.need_name())
        self.assertTrue(register.need_description())
        self.assertTrue(register.need_type())

        self.empty_command.payment_date = 2

        self.assertTrue(register.need_payment_installments())
        self.assertTrue(register.need_entry_date())
        self.assertFalse(register.need_payment_date())
        self.assertTrue(register.need_debit())
        self.assertTrue(register.need_credit())
        self.assertTrue(register.need_category())
        self.assertTrue(register.need_name())
        self.assertTrue(register.need_description())
        self.assertTrue(register.need_type())

    def test_should_return_false_for_all_options(self):

        register = Register(self.completed_command)

        self.assertFalse(register.need_payment_installments())
        self.assertFalse(register.need_entry_date())
        self.assertFalse(register.need_payment_date())
        self.assertFalse(register.need_debit())
        self.assertFalse(register.need_credit())
        self.assertFalse(register.need_category())
        self.assertFalse(register.need_name())
        self.assertFalse(register.need_description())
        self.assertFalse(register.need_type())
