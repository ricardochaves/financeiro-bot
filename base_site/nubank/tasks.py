from base_site.nubank.models import NubankStatement


def process_nubank_statements():
    statements = NubankStatement.objects.filter(is_processed=False).all()

    for s in statements:

        charges = s.details.get("charges")

        if charges:
            # {"count": 2, "amount": 6095}
            count = charges.get("count")
