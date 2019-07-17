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

    def next(self, value):

        if not self.start:
            self.start = True
            return self._get_next()

        self._set_next(value)
        return self._get_next()

    def _set_next(self, value):

        if self.register.need_debit():
            logging.debug(f"SET need_debit: {value}")
            self.register.val_debit = Decimal(value)

        elif self.register.need_credit():
            logging.debug(f"SET need_credit: {value}")
            self.register.val_credit = Decimal(value)

        elif self.register.need_description():
            logging.debug(f"SET need_description: {value}")
            self.register.description = value

        elif self.register.need_entry_date():
            logging.debug(f"SET need_entry_date: {value}")
            self.register.entry_date_value = self.cal.convert_calendar_day_value_to_datetime(value)

        elif self.register.need_payment_date():
            logging.debug(f"SET need_payment_date: {value}")
            self.register.payment_date_value = self.cal.convert_calendar_day_value_to_datetime(
                value
            )
        elif self.register.need_category():
            logging.debug(f"SET need_category: {value}")
            self.register.category = value

        elif self.register.need_name():
            logging.debug(f"SET need_name: {value}")
            self.register.name = value

        elif self.register.need_type():
            logging.debug(f"SET need_type: {value}")
            self.register.type_entry = value

        elif self.register.need_payment_installments():
            logging.debug(f"SET need_payment_installments: {value}")
            self.register.payment_installments = value

    def _get_next(self):

        data = {"done": True}

        if self.register.need_debit():
            logging.debug("GET need_debit")
            data = self._build_data(message="Informe o valor de débito")

        elif self.register.need_credit():
            logging.debug("GET need_credit")
            data = self._build_data(message="Informe o valor de crédito")

        elif self.register.need_description():
            logging.debug("GET need_description")
            data = self._build_data(message="Informe a descrição")

        elif self.register.need_entry_date():
            logging.debug("GET need_entry_date")
            data = self._build_data(
                keyboard=self.command_keyboard.get_entry_date(),
                message="Informe a data de lançamento",
            )

        elif self.register.need_payment_date():
            logging.debug("GET need_payment_date")
            data = self._build_data(
                keyboard=self.command_keyboard.get_payment_date(),
                message="Informe a data de pagamento",
            )

        elif self.register.need_category():
            logging.debug("GET need_category")
            data = self._build_data(
                keyboard=self.command_keyboard.get_category(), message="Informe a categoria"
            )

        elif self.register.need_name():
            logging.debug("GET need_name")
            data = self._build_data(
                keyboard=self.command_keyboard.get_name(), message="Informe o nome"
            )

        elif self.register.need_type():
            logging.debug("GET need_type")
            data = self._build_data(
                keyboard=CommandKeyBoard.get_need_type(), message="Informe o tipo"
            )

        elif self.register.need_payment_installments():
            logging.debug("GET need_payment_installments")
            data = self._build_data(
                keyboard=CommandKeyBoard.get_payment_installments(),
                message="Informe o número de parcelas",
            )

        return data

    @staticmethod
    def _build_data(keyboard=None, message=None):
        data = {"keyboard": keyboard, "message": message, "done": False}
        return data

    def save(self):
        self.register.save()
