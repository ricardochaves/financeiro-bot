from django.test import TestCase
from django.utils import timezone

from base_site.mainapp.goals import get_goals
from base_site.mainapp.models import Goal
from base_site.mainapp.models import Records
from tests.helper import create_scenario_with_two_commands_complete_and_empty


class GoalTestCase(TestCase):
    def setUp(self):
        self.category, self.family_member, self.type_entry, self.empty_command, self.completed_command = (
            create_scenario_with_two_commands_complete_and_empty()
        )

    def test_should_return_goal(self):

        Records.objects.create(
            create_date_time=timezone.now(),
            payment_date_time=timezone.now(),
            debit=200,
            category=self.category,
            name=self.family_member,
            type_entry=self.type_entry,
        )

        Records.objects.create(
            create_date_time=timezone.now(),
            payment_date_time=timezone.now(),
            debit=50,
            category=self.category,
            name=self.family_member,
            type_entry=self.type_entry,
        )

        Goal.objects.create(
            category=self.category,
            name_family=self.family_member,
            type_entry=self.type_entry,
            name="goal_1",
            value=100,
            period=1,
        )

        g_list = get_goals()

        self.assertEqual(len(g_list), 1)
