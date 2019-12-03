import json
import uuid
from decimal import Decimal

from pynubank import Nubank
from qrcode.image.pil import PilImage

from base_site.nubank.models import NubankBankStatement
from base_site.nubank.models import NubankCards
from base_site.nubank.models import NubankSession
from base_site.nubank.models import NubankStatement
from base_site.settings import NUBANK_CPF
from dateutil.parser import parse
from django.utils import timezone


class NubankBot:
    nu = None
    logged = False
    n_card = None

    def __init__(self):
        self.nu = Nubank()

    def set_nubank_command(self, n: NubankCards):
        self.n_card = n

    def get_qr_code(self):

        uid, qr_code = self.nu.get_qr_code()
        img: PilImage = qr_code.make_image()

        NubankSession.objects.update_or_create(session_id=uid, defaults={"session_id": uid})

        name = f"./{uuid.uuid4().hex}.png"
        img.save(name)

        qr_code.print_ascii(invert=True)

        return name

    def _login(self, pwd: str):

        last_login_diff = timezone.now() - self.n_card.last_login
        total_hours = last_login_diff.total_seconds() / 3600
        if total_hours < 12:
            raise Exception("You can't login now")

        nu_session = NubankSession.objects.order_by("-created_at").first()

        self.nu.authenticate_with_qr_code(self.n_card.cpf, pwd, nu_session.session_id)
        self.logged = True
        self.n_card.last_login = timezone.now()
        self.n_card.save()

    def execute(self, pwd: str):

        if not self.logged:
            self._login(pwd)

        card_statements = self.nu.get_card_statements()

        for n in card_statements:

            amount_without_iof = 0
            if n.get("amount_without_iof"):
                amount_without_iof = Decimal(n["amount_without_iof"]) / 100

            defaults = {
                "amount": Decimal(n["amount"]) / 100,
                "amount_without_iof": amount_without_iof,
                "description": n.get("description"),
                "category": n.get("category"),
                "source": n.get("source"),
                "title": n.get("title"),
                "account": n.get("account"),
                "details": n.get("details"),
                "nubank_id": n["id"],
                "href": n.get("href"),
                "item_time": parse(n["time"]),
            }

            NubankStatement.objects.get_or_create(nubank_id=n["id"], defaults=defaults)

        self._execute_bank_statements()

        return

    def _execute_bank_statements(self):
        account_statements = self.nu.get_account_statements()

        for a in account_statements:
            if a["__typename"] == "TransferOutReversalEvent":
                continue

            defaults = {
                "nubank_id": a["id"],
                "title": a["title"],
                "detail": a["detail"],
                "amount": Decimal(a["amount"]),
                "post_date": a["postDate"],
                "_type": a["__typename"],
            }
            NubankBankStatement.objects.get_or_create(nubank_id=a["id"], defaults=defaults)
