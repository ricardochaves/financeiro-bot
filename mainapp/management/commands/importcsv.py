import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand

from mainapp.models import Category
from mainapp.models import FamilyMember
from mainapp.models import Records
from mainapp.models import TypeEntry


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Records.objects.all().delete()
        with open("Financeiro Casal - Fluxo Caixa.tsv", newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter="\t", quotechar="|")
            for row in spamreader:
                if row[0]:
                    r = Records()
                    r.create_date_time = datetime.strptime(row[0], "%d/%m/%Y").astimezone()
                    r.payment_date_time = datetime.strptime(row[1], "%d/%m/%Y").astimezone()

                    r.debit = Decimal(row[2].replace(",", ".")) if row[2] else None
                    r.credit = Decimal(row[3].replace(",", ".")) if row[3] else None

                    category = Category.objects.filter(name=row[5]).first()
                    r.category = category

                    name = FamilyMember.objects.filter(name=row[6]).first()
                    r.name = name

                    r.description = row[7]

                    entrytype = TypeEntry.objects.filter(name=row[8]).first()
                    r.type_entry = entrytype

                    r.save()
