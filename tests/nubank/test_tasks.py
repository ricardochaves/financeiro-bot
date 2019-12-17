import uuid
from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import Records
from base_site.mainapp.models import TypeEntry
from base_site.nubank.models import NubankBankStatement
from base_site.nubank.models import NubankCards
from base_site.nubank.models import NubankItemSetup
from base_site.nubank.models import NubankStatement
from base_site.nubank.tasks import get_setup
from base_site.nubank.tasks import process_nubank_bank_statements
from base_site.nubank.tasks import process_nubank_statements


class NubankTaskTestCase(TestCase):
    def setUp(self) -> None:

        self.category = Category.objects.create(name="test")
        self.name = FamilyMember.objects.create(name="test")
        self.type_entry = TypeEntry.objects.create(name="test")

        self.card = NubankCards.objects.create(command_1="1", command_2="1a", cpf="87654678976", name=self.name)

        self.setup = self._crete_setup()

    def _crete_setup(self, desc: str = "slug-1", check_value=None, check_value_operator=None) -> NubankItemSetup:
        return NubankItemSetup.objects.create(
            description=desc,
            description_slug=desc,
            category=self.category,
            name=self.name,
            type_entry=self.type_entry,
            check_value=check_value,
            check_value_operator=check_value_operator,
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

        self._crete_setup(check_value=90, check_value_operator=">")

        NubankBankStatement.objects.create(
            created_at=timezone.now(),
            nubank_id=uuid.uuid4(),
            title="slug-1",
            detail="detail 1",
            amount=100,
            post_date=timezone.now().date(),
            _type="TransferInEvent",
            cpf="87654678976",
        )

        process_nubank_bank_statements()
        process_nubank_bank_statements()

        self.assertEqual(Records.objects.count(), 1)

        i = Records.objects.first()
        self.assertEqual(i.credit, 100)

    def test_should_create_debit_record_from_bank(self):

        self._crete_setup(check_value=100, check_value_operator="=")

        NubankBankStatement.objects.create(
            created_at=timezone.now(),
            nubank_id=uuid.uuid4(),
            title="slug-1",
            detail="detail 1",
            amount=100,
            post_date=timezone.now().date(),
            _type="TransferOutEvent",
            cpf="87654678976",
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
            cpf="87654678976",
        )

        process_nubank_bank_statements()

        self.assertEqual(Records.objects.count(), 0)

    def test_should_return_setup_when_value_is_given(self):

        self._crete_setup(check_value=100, check_value_operator="<")

        setup = get_setup("slug-1", self.name, 150)

        self.assertIsNone(setup)

        setup = get_setup("slug-1", self.name, 99)
        self.assertIsNotNone(setup)

        self._crete_setup(check_value=250, check_value_operator="=")
        self.assertIsNotNone(setup)

        self._crete_setup(check_value=200, check_value_operator=">")
        setup = get_setup("slug-1", self.name, 300)

        self.assertIsNotNone(setup)

    def test_should_return_setup_when_setup_dont_have_check_name(self):

        setup = get_setup("slug-1", self.name)

        self.assertIsNotNone(setup)

        setup = get_setup("slug-1", FamilyMember.objects.create(name="hi"))

        self.assertIsNotNone(setup)

    def test_should_return_setup_when_name_is_given(self):
        self.setup.check_name = self.name
        self.setup.save()

        setup = get_setup("slug-1", self.name)

        self.assertIsNotNone(setup)

        setup = get_setup("slug-1", FamilyMember.objects.create(name="hi"))

        self.assertIsNone(setup)

    def test_should_not_create_credit_record_from_bank(self):

        self._crete_setup(check_value=150, check_value_operator=">")

        NubankBankStatement.objects.create(
            created_at=timezone.now(),
            nubank_id=uuid.uuid4(),
            title="slug-1",
            detail="detail 1",
            amount=100,
            post_date=timezone.now().date(),
            _type="TransferInEvent",
            cpf="87654678976",
        )

        process_nubank_bank_statements()
        process_nubank_bank_statements()

        self.assertEqual(Records.objects.count(), 0)
