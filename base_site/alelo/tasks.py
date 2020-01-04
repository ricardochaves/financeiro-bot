from datetime import datetime

from django.db import transaction
from python_alelo.alelo import Alelo
from python_alelo.alelo import TransactionsTime

from base_site.alelo.models import AleloCard
from base_site.alelo.models import AleloItem
from base_site.alelo.models import AleloItemSetup
from base_site.mainapp.models import Records
from base_site.settings import ALELO_CPF
from base_site.settings import ALELO_PASSWORD


def execute_alelo_api():

    numbers = [c.last_numbers for c in AleloCard.objects.all()]

    a = Alelo(cpf=ALELO_CPF, pwd=ALELO_PASSWORD)
    a.login()

    cards = a.get_cards()

    for c in cards:
        if c.last_numbers in numbers:
            transactions = a.get_transactions(c, TransactionsTime.LAST_FOUR_MONTHS)

            for t in transactions["transactions"]:
                item_date_time = datetime.strptime(t["date"] + "/" + str(datetime.now().year), "%d/%m/%Y")
                item_date = item_date_time.date()

                defaults = {
                    "item_date": item_date,
                    "value": t["value"],
                    "item_type": t["type"],
                    "icon": t["icon"],
                    "description": t["description"],
                }

                AleloItem.objects.get_or_create(
                    item_date=item_date,
                    value=t["value"],
                    item_type=t["type"],
                    icon=t["icon"],
                    description=t["description"],
                    defaults=defaults,
                )


def check_items():

    items = AleloItem.objects.filter(is_processed=False).all()

    for i in items:

        new_desc = i.description.strip().lower()

        config = AleloItemSetup.objects.filter(description__contains=new_desc).first()

        if config:

            with transaction.atomic():
                i.is_processed = True
                i.save()

                Records.objects.create(
                    create_date_time=i.item_date,
                    payment_date_time=i.item_date,
                    debit=i.value if not config.is_credit else 0,
                    credit=i.value if config.is_credit else 0,
                    category=config.category,
                    name=config.name,
                    type_entry=config.type_entry,
                    description=i.description,
                )
