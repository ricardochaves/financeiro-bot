from pynubank import Nubank

from base_site.settings import NUBANK_CPF
from base_site.settings import NUBANK_PASSWORD
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        nu = Nubank()
        uuid, qr_code = nu.get_qr_code()

        qr_code.print_ascii(invert=True)

        nu.authenticate_with_qr_code(NUBANK_CPF, NUBANK_PASSWORD, uuid)
        print(nu.get_account_balance())

        card_statements = nu.get_card_statements()
