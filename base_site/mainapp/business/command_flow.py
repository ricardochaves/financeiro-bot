import logging
from decimal import Decimal

from base_site.mainapp.business.register import Register
from base_site.mainapp.command_keyboard import CommandKeyBoard
from base_site.mainapp.models import FullCommand
from base_site.mainapp.telegram_bot.calendar import Calendar

logger = logging.getLogger(__name__)


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
            logger.debug("SET need_debit: %s", value)
            self.register.val_debit = Decimal(value)

        elif self.register.need_credit():
            logger.debug("SET need_credit: %s", value)
            self.register.val_credit = Decimal(value)

        elif self.register.need_description():
            logger.debug("SET need_description: %s", value)
            self.register.description = value

        elif self.register.need_entry_date():
            logger.debug("SET need_entry_date: %s", value)
            self.register.entry_date_value = self.cal.convert_calendar_day_value_to_datetime(value)

        elif self.register.need_payment_date():
            logger.debug("SET need_payment_date: %s", value)
            self.register.payment_date_value = self.cal.convert_calendar_day_value_to_datetime(value)
        elif self.register.need_category():
            logger.debug("SET need_category: %s", value)
            self.register.category = value

        elif self.register.need_name():
            logger.debug("SET need_name: %s", value)
            self.register.name = value

        elif self.register.need_type():
            logger.debug("SET need_type: %s", value)
            self.register.type_entry = value

        elif self.register.need_payment_installments():
            logger.debug("SET need_payment_installments: %s", value)
            self.register.payment_installments = value

    def _get_next(self):

        data = {"done": True}

        if self.register.need_debit():
            logger.debug("GET need_debit")
            data = self._build_data(message="Informe o valor de débito")

        elif self.register.need_credit():
            logger.debug("GET need_credit")
            data = self._build_data(message="Informe o valor de crédito")

        elif self.register.need_description():
            logger.debug("GET need_description")
            data = self._build_data(message="Informe a descrição")

        elif self.register.need_entry_date():
            logger.debug("GET need_entry_date")
            data = self._build_data(
                keyboard=self.command_keyboard.get_entry_date(), message="Informe a data de lançamento"
            )

        elif self.register.need_payment_date():
            logger.debug("GET need_payment_date")
            data = self._build_data(
                keyboard=self.command_keyboard.get_payment_date(), message="Informe a data de pagamento"
            )

        elif self.register.need_category():
            logger.debug("GET need_category")
            data = self._build_data(keyboard=self.command_keyboard.get_category(), message="Informe a categoria")

        elif self.register.need_name():
            logger.debug("GET need_name")
            data = self._build_data(keyboard=self.command_keyboard.get_name(), message="Informe o nome")

        elif self.register.need_type():
            logger.debug("GET need_type")
            data = self._build_data(keyboard=CommandKeyBoard.get_need_type(), message="Informe o tipo")

        elif self.register.need_payment_installments():
            logger.debug("GET need_payment_installments")
            data = self._build_data(
                keyboard=CommandKeyBoard.get_payment_installments(), message="Informe o número de parcelas"
            )

        return data

    @staticmethod
    def _build_data(keyboard=None, message=None):
        data = {"keyboard": keyboard, "message": message, "done": False}
        return data

    def save(self):
        self.register.save()
