from base_site.alelo.models import AleloItem
from base_site.alelo.models import AleloItemSetup
from base_site.mainapp.models import Records
from django.db import transaction


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
