from typing import Tuple

from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import FullCommand
from base_site.mainapp.models import TypeEntry


def create_scenario_with_two_commands_complete_and_empty() -> Tuple[
    Category, FamilyMember, TypeEntry, FullCommand, FullCommand
]:
    category = Category.objects.create(name="cat_1")
    family_member = FamilyMember.objects.create(name="member_1")
    type_entry = TypeEntry.objects.create(name="type_1")
    empty_command = FullCommand.objects.create(command="/a", entry_date=False, payment_date=3)
    completed_command = FullCommand.objects.create(
        command="/just_do",
        entry_date=True,
        payment_date=1,
        debit=10,
        credit=0,
        category=category,
        name=family_member,
        description="hi",
        type_entry=type_entry,
    )

    return category, family_member, type_entry, empty_command, completed_command
