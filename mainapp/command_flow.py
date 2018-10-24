import logging
import sys
from decimal import Decimal

from mainapp.calendar import Calendar
from mainapp.command_keyboard import CommandKeyBoard
from mainapp.models import FullCommand
from mainapp.register import Register

logging.basicConfig(stream=sys.stdout)


class CommandFlow:
    def __init__(self, txt_command):
        self.register = Register(FullCommand.objects.filter(command=txt_command).first())
        self.start = False
        self.cal = Calendar()
        self.command_keyboard = CommandKeyBoard(self.cal)

    def next(self, txt_command):

        if not self.start:
            self.start = True
            return self._get_next()

        self._set_next(txt_command)
        return self._get_next()

    def _set_next(self, txt_command):

        if self.register.need_debit():
            logging.warning(f"SET need_debit: {txt_command}")
            self.register.val_debit = Decimal(txt_command)

        elif self.register.need_credit():
            logging.warning(f"SET need_credit: {txt_command}")
            self.register.val_credit = Decimal(txt_command)

        elif self.register.need_description():
            logging.warning(f"SET need_description: {txt_command}")
            self.register.description = txt_command

        elif self.register.need_entry_date():
            logging.warning(f"SET need_entry_date: {txt_command}")
            self.register.entry_date_value = self.cal.convert_calendar_day_value_to_datetime(txt_command)

        elif self.register.need_payment_date():
            logging.warning(f"SET need_payment_date: {txt_command}")
            self.register.payment_date_value = self.cal.convert_calendar_day_value_to_datetime(txt_command)

        elif self.register.need_category():
            logging.warning(f"SET need_category: {txt_command}")
            self.register.category = txt_command

        elif self.register.need_name():
            logging.warning(f"SET need_name: {txt_command}")
            self.register.name = txt_command

        elif self.register.need_type():
            logging.warning(f"SET need_type: {txt_command}")
            self.register.type_entry = txt_command

        elif self.register.need_payment_installments():
            logging.warning(f"SET need_payment_installments: {txt_command}")
            self.register.payment_installments = txt_command

    def _get_next(self):

        data = {"done": True}

        if self.register.need_debit():
            logging.warning("GET need_debit")
            data = self._build_data(message="Informe o valor de débito")

        elif self.register.need_credit():
            logging.warning("GET need_credit")
            data = self._build_data(message="Informe o valor de crédito")

        elif self.register.need_description():
            logging.warning("GET need_description")
            data = self._build_data(message="Informe a descrição")

        elif self.register.need_entry_date():
            logging.warning("GET need_entry_date")
            data = self._build_data(
                keyboard=self.command_keyboard.get_entry_date(), message="Informe a data de lançamento"
            )

        elif self.register.need_payment_date():
            logging.warning("GET need_payment_date")
            data = self._build_data(
                keyboard=self.command_keyboard.get_payment_date(), message="Informe a data de pagamento"
            )

        elif self.register.need_category():
            logging.warning("GET need_category")
            data = self._build_data(keyboard=self.command_keyboard.get_category(), message="Informe a categoria")

        elif self.register.need_name():
            logging.warning("GET need_name")
            data = self._build_data(keyboard=self.command_keyboard.get_name(), message="Informe o nome")

        elif self.register.need_type():
            logging.warning("GET need_type")
            data = self._build_data(keyboard=CommandKeyBoard.get_need_type(), message="Informe o tipo")

        elif self.register.need_payment_installments():
            logging.warning("GET need_payment_installments")
            data = self._build_data(
                keyboard=CommandKeyBoard.get_payment_installments(), message="Informe o número de parcelas"
            )

        return data

    @staticmethod
    def _build_data(keyboard=None, message=None):
        data = {}
        data["keyboard"] = keyboard
        data["message"] = message
        data["done"] = False
        return data

    def save(self):
        self.register.save()
