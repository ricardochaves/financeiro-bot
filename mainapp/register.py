import logging
import sys
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from mainapp.google_service import Google
from mainapp.models import Category
from mainapp.models import FamilyMember
from mainapp.models import FullCommand
from mainapp.models import Records
from mainapp.models import TypeEntry
from pytz import timezone

logging.basicConfig(stream=sys.stdout)


class Register:
    def __init__(self, full_command: FullCommand):
        self.full_command = full_command
        self.entry_date_value = None
        self.payment_date_value = None
        self.val_debit = full_command.debit
        self.val_credit = full_command.credit
        self.category = full_command.category
        self.name = full_command.name
        self.description = full_command.description
        self.type_entry = full_command.type_entry
        self.payment_installments = None

    def need_payment_installments(self):
        return (self.full_command.payment_date == 2) and (not self.payment_installments)

    def need_entry_date(self):
        return (not self.full_command.entry_date) and (not self.entry_date_value)

    def need_payment_date(self):
        return (self.full_command.payment_date == 3) and (not self.payment_date_value)

    def need_debit(self):
        return self.val_debit is None

    def need_credit(self):
        return self.val_credit is None

    def need_category(self):
        return self.category is None

    def need_name(self):
        return self.name is None

    def need_description(self):
        return self.description == ""

    def need_type(self):
        return self.type_entry is None

    def _calc_payments(self):

        if self.full_command.payment_date != 2:
            return [
                {
                    "date": self._get_payment_date_value(),
                    "credit": self.val_credit,
                    "debit": self.val_debit,
                    "description": "",
                }
            ]

        payments = []

        final_credit_val = 0
        if self.val_credit:
            final_credit_val = str(Decimal(self.val_credit) / int(self.payment_installments))

        final_debit_val = 0
        if self.val_debit:
            final_debit_val = str(Decimal(self.val_debit) / int(self.payment_installments))

        for p in range(int(self.payment_installments)):
            payments.append(
                {
                    "date": self._calc_payment_date(p),
                    "credit": final_credit_val,
                    "debit": final_debit_val,
                    "description": f" ({p+1} de {self.payment_installments})",
                }
            )

        return payments

    def _calc_payment_date(self, count):
        if not count:
            return self._get_payment_date_value()

        work_date = self._get_date(self._get_payment_date_value())
        work_date = work_date + relativedelta(months=+(count))
        return work_date.strftime("%d/%m/%Y")

    def save(self):

        payments = self._calc_payments()
        for p in payments:
            self._send_google(p["date"], p["credit"], p["debit"], p["description"])
            self._save_on_database(p["date"], p["credit"], p["debit"], p["description"])

    def _send_google(self, date, val_credit, val_debt, description):

        values = "%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
            self._get_entry_date_value(),
            date,
            str(val_debt).replace(".", ","),
            str(val_credit).replace(".", ","),
            "",
            self.category,
            self.name,
            self.description + description,
            self.type_entry,
        )
        logging.warning(f"Valores para a planilha: {values}")
        logging.warning(Google().append_values(values))

    def _save_on_database(self, date, val_credit, val_debt, description):
        Records.objects.create(
            create_date_time=self._get_date(self._get_entry_date_value()),
            payment_date_time=self._get_date(date),
            debit=val_debt,
            credit=val_credit,
            category=self._get_category(self.category),
            name=self._get_family_membor(self.name),
            type_entry=self._get_type_entry(self.type_entry),
            description=self.description + description,
        )

    @staticmethod
    def _get_date(dt):
        return datetime.strptime(f"{dt}", "%d/%m/%Y").astimezone(timezone("America/Sao_Paulo"))

    @staticmethod
    def _get_type_entry(type_name):
        return TypeEntry.objects.filter(name=type_name).first()

    @staticmethod
    def _get_family_membor(family_name):
        return FamilyMember.objects.filter(name=family_name).first()

    @staticmethod
    def _get_category(category):
        return Category.objects.filter(name=category).first()

    def _get_entry_date_value(self):
        if self.full_command.entry_date:  # True = Data do dia
            return datetime.now().astimezone(timezone("America/Sao_Paulo")).strftime("%d/%m/%Y")

        # Else, veio do Bot
        return self.entry_date_value.strftime("%d/%m/%Y")

    def _get_payment_date_value(self):

        if self.full_command.payment_date == 1:  # Data do Dia
            return datetime.now().astimezone(timezone("America/Sao_Paulo")).strftime("%d/%m/%Y")

        if self.full_command.payment_date == 2:  # Data do Cartão (15)

            work_data = self._get_date(self._get_entry_date_value())
            if work_data.day >= 8:
                next_month = work_data + relativedelta(months=+1)
                return f"15/{next_month.month}/{next_month.year}"
            else:
                return f"15/{work_data.month}/{work_data.year}"

        if self.full_command.payment_date == 4:  # Dia Seguinte
            work_data = self._get_date(self._get_entry_date_value())
            next_day = work_data + relativedelta(days=+1)
            return next_day.strftime("%d/%m/%Y")

        if self.full_command.payment_date == 5:  # Mês Seguinte
            work_data = self._get_date(self._get_entry_date_value())
            next_month = work_data + relativedelta(months=+1)
            return next_month.strftime("%d/%m/%Y")

        if self.full_command.payment_date == 6:  # Dia 5 mês vigente
            work_data = self._get_date(self._get_entry_date_value())
            return next_month.strftime("5/%m/%Y")

        if self.full_command.payment_date == 7:  # Dia 5 mês que vem
            work_data = self._get_date(self._get_entry_date_value())
            next_month = work_data + relativedelta(months=+1)
            return next_month.strftime("5/%m/%Y")

        # Else, veio do Bot
        return self.payment_date_value.strftime("%d/%m/%Y")
