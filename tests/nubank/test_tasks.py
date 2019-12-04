import uuid
from datetime import datetime

from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import Records
from base_site.mainapp.models import TypeEntry
from base_site.nubank.models import NubankBankStatement
from base_site.nubank.models import NubankItemSetup
from base_site.nubank.models import NubankStatement
from base_site.nubank.tasks import process_nubank_bank_statements
from base_site.nubank.tasks import process_nubank_statements
from django.test import TestCase
from django.utils import timezone


class NubankTaskTestCase(TestCase):
    def setUp(self) -> None:

        self.category = Category.objects.create(name="test")
        self.name = FamilyMember.objects.create(name="test")
        self.type_entry = TypeEntry.objects.create(name="test")

        NubankItemSetup.objects.create(
            description="slug-1",
            description_slug="slug-1",
            category=self.category,
            name=self.name,
            type_entry=self.type_entry,
        )

    def test_should_create_one_record_whit_same_month(self):

        NubankStatement.objects.create(amount=100, description="slug-1", item_time=datetime(2019, 1, 7), details={})

        process_nubank_statements()

        record = Records.objects.first()

        self.assertEqual(Records.objects.count(), 1)

        self.assertEqual(record.name, self.name)
        self.assertEqual(record.category, self.category)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertEqual(record.debit, 100)
        self.assertIsNone(record.credit)

        self.assertEqual(record.description, "slug-1")

        self.assertEqual(record.payment_date_time.day, 15)
        self.assertEqual(record.payment_date_time.month, 1)
        self.assertEqual(record.payment_date_time.year, 2019)

    def test_should_create_one_record_whit_next_month(self):

        NubankStatement.objects.create(amount=100, description="slug-1", item_time=datetime(2019, 1, 9), details={})

        process_nubank_statements()

        record = Records.objects.first()

        self.assertEqual(Records.objects.count(), 1)

        self.assertEqual(record.name, self.name)
        self.assertEqual(record.category, self.category)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertEqual(record.debit, 100)
        self.assertIsNone(record.credit)

        self.assertEqual(record.description, "slug-1")

        self.assertEqual(record.payment_date_time.day, 15)
        self.assertEqual(record.payment_date_time.month, 2)
        self.assertEqual(record.payment_date_time.year, 2019)

    def test_should_create_two_records_whit_first_in_same_month(self):

        NubankStatement.objects.create(
            amount=100,
            description="slug-1",
            item_time=datetime(2019, 1, 7),
            details={"charges": {"amount": 5000, "count": 2}},
        )

        process_nubank_statements()

        record = Records.objects.order_by("payment_date_time").first()

        self.assertEqual(Records.objects.count(), 2)

        self.assertEqual(record.name, self.name)
        self.assertEqual(record.category, self.category)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertEqual(record.debit, 50)
        self.assertIsNone(record.credit)

        self.assertEqual(record.description, "slug-1")

        self.assertEqual(record.payment_date_time.day, 15)
        self.assertEqual(record.payment_date_time.month, 1)
        self.assertEqual(record.payment_date_time.year, 2019)

        record = Records.objects.order_by("-payment_date_time").first()

        self.assertEqual(record.name, self.name)
        self.assertEqual(record.category, self.category)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertEqual(record.debit, 50)
        self.assertIsNone(record.credit)

        self.assertEqual(record.description, "slug-1")

        self.assertEqual(record.payment_date_time.day, 15)
        self.assertEqual(record.payment_date_time.month, 2)
        self.assertEqual(record.payment_date_time.year, 2019)

    def test_should_create_two_records_whit_first_in_next_month(self):

        NubankStatement.objects.create(
            amount=100,
            description="slug-1",
            item_time=datetime(2019, 1, 9),
            details={"charges": {"amount": 5000, "count": 2}},
        )

        process_nubank_statements()

        record = Records.objects.order_by("payment_date_time").first()

        self.assertEqual(Records.objects.count(), 2)

        self.assertEqual(record.name, self.name)
        self.assertEqual(record.category, self.category)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertEqual(record.debit, 50)
        self.assertIsNone(record.credit)

        self.assertEqual(record.description, "slug-1")

        self.assertEqual(record.payment_date_time.day, 15)
        self.assertEqual(record.payment_date_time.month, 2)
        self.assertEqual(record.payment_date_time.year, 2019)

        record = Records.objects.order_by("-payment_date_time").first()

        self.assertEqual(record.name, self.name)
        self.assertEqual(record.category, self.category)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertEqual(record.debit, 50)
        self.assertIsNone(record.credit)

        self.assertEqual(record.description, "slug-1")

        self.assertEqual(record.payment_date_time.day, 15)
        self.assertEqual(record.payment_date_time.month, 3)
        self.assertEqual(record.payment_date_time.year, 2019)

    def test_should_create_credit_record_from_bank(self):

        NubankBankStatement.objects.create(
            created_at=timezone.now(),
            nubank_id=uuid.uuid4(),
            title="slug-1",
            detail="detail 1",
            amount=100,
            post_date=timezone.now().date(),
            _type="TransferInEvent",
        )

        process_nubank_bank_statements()
        process_nubank_bank_statements()

        self.assertEqual(Records.objects.count(), 1)

        i = Records.objects.first()
        self.assertEqual(i.credit, 100)

    def test_should_create_debit_record_from_bank(self):

        NubankBankStatement.objects.create(
            created_at=timezone.now(),
            nubank_id=uuid.uuid4(),
            title="slug-1",
            detail="detail 1",
            amount=100,
            post_date=timezone.now().date(),
            _type="TransferOutEvent",
        )

        process_nubank_bank_statements()
        process_nubank_bank_statements()

        self.assertEqual(Records.objects.count(), 1)

        i = Records.objects.first()
        self.assertEqual(i.debit, 100)

    def test_should_not_create_record_from_bank(self):

        NubankBankStatement.objects.create(
            created_at=timezone.now(),
            nubank_id=uuid.uuid4(),
            title="slug-1",
            detail="detail 1",
            amount=100,
            post_date=timezone.now().date(),
            _type="NOT_FOUND",
        )

        process_nubank_bank_statements()

        self.assertEqual(Records.objects.count(), 0)
