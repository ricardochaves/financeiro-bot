from datetime import datetime

from python_alelo.alelo import Alelo
from python_alelo.alelo import TransactionsTime

from base_site.alelo.models import AleloItem
from base_site.settings import ALELO_CARD_LAST_NUMBER
from base_site.settings import ALELO_CPF
from base_site.settings import ALELO_PASSWORD
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        a = Alelo(cpf=ALELO_CPF, pwd=ALELO_PASSWORD)
        a.login()

        cards = a.get_cards()

        for c in cards:
            if c["lastNumbers"] == ALELO_CARD_LAST_NUMBER:
                transactions = a.get_transactions(c["id"], TransactionsTime.LAST_FOUR_MONTHS)

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
