from datetime import datetime
from decimal import Decimal

from base_site.alelo.models import AleloItem
from base_site.alelo.models import AleloItemSetup
from base_site.alelo.tasks import check_items
from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import Records
from base_site.mainapp.models import TypeEntry
from django.test import TestCase


class AleloTasksTestCase(TestCase):
    def setUp(self) -> None:

        self.category = Category.objects.create(name="test")
        self.name = FamilyMember.objects.create(name="test")
        self.type_entry = TypeEntry.objects.create(name="test")

    def test_check_items_should_create_just_items_with_config_with_debit(self):
        a_1 = AleloItem.objects.create(
            item_date=datetime.now().date(), value=100.20, item_type="DEBIT", icon="shopping", description="RES com "
        )

        a_2 = AleloItem.objects.create(
            item_date=datetime.now().date(), value=100.20, item_type="DEBIT", icon="shopping", description="XPTO"
        )

        AleloItemSetup.objects.create(
            description="res com", category=self.category, name=self.name, type_entry=self.type_entry
        )

        check_items()
        a_1.refresh_from_db()
        a_2.refresh_from_db()

        self.assertEqual(Records.objects.count(), 1)

        record = Records.objects.first()

        self.assertAlmostEqual(record.debit, Decimal(100.20))
        self.assertAlmostEqual(record.credit, Decimal(0))

        self.assertEqual(record.category, self.category)
        self.assertEqual(record.name, self.name)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertFalse(a_2.is_processed)
        self.assertTrue(a_1.is_processed)

    def test_check_items_should_create_just_items_with_config_with_credit(self):
        a_1 = AleloItem.objects.create(
            item_date=datetime.now().date(), value=100.20, item_type="DEBIT", icon="shopping", description="RES com "
        )

        a_2 = AleloItem.objects.create(
            item_date=datetime.now().date(), value=100.20, item_type="DEBIT", icon="shopping", description="XPTO"
        )

        AleloItemSetup.objects.create(
            description="res com", category=self.category, name=self.name, type_entry=self.type_entry, is_credit=True
        )

        check_items()
        a_1.refresh_from_db()
        a_2.refresh_from_db()

        self.assertEqual(Records.objects.count(), 1)

        record = Records.objects.first()

        self.assertAlmostEqual(record.debit, Decimal(0))
        self.assertAlmostEqual(record.credit, Decimal(100.20))

        self.assertEqual(record.category, self.category)
        self.assertEqual(record.name, self.name)
        self.assertEqual(record.type_entry, self.type_entry)

        self.assertFalse(a_2.is_processed)
        self.assertTrue(a_1.is_processed)
