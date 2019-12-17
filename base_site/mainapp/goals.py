import asyncio
import datetime
import logging
from typing import Tuple

from django.conf import settings
from django.db.models import Func
from django.db.models import IntegerField
from django.db.models import Sum

import telepot
from base_site.mainapp.models import Goal
from base_site.mainapp.models import Records
from isoweek import Week


class YearWeek(Func):
    function = "YEARWEEK"
    template = "%(function)s(%(expressions)s)"
    output_field = IntegerField()


class CalculateGoals:
    def __init__(self, user_id):
        self.user_id = user_id

    def execute_goals(self):

        week_day = datetime.datetime.now().isocalendar()[1]
        w = Week(datetime.datetime.now().year, week_day)
        start_date = w.monday()
        end_date = w.sunday()

        result = Records.objects.filter(
            create_date_time__date__range=(start_date, end_date), type_entry__id=1
        ).annotate(total_value=Sum("debit"))

        try:

            total_debit = 0
            for a in result:
                total_debit += a.total_value if a.total_value else 0

            logging.warning(f"total_debit: {total_debit}")

            can_use = 770 - total_debit

            loop = asyncio.get_event_loop()

            bot = telepot.aio.Bot(settings.TELEGRAM_TOKEN)

            loop.run_until_complete(
                bot.sendMessage(
                    self.user_id, f"Você ainda pode gastar {can_use} doas 770 reais estipulados para a semana."
                )
            )

        except BaseException as e:
            logging.exception("Error na meta", e)


def get_goals():

    goals = Goal.objects.filter(enable=True).all()
    data = []

    for g in goals:
        init_date, end_date = get_ini_and_end_date(g)

        qs = Records.objects.all()

        qs = qs.filter(create_date_time__date__range=(init_date, end_date))

        if g.category:
            qs.filter(category=g.category)

        if g.name_family:
            qs.filter(name=g.name_family)

        if g.type_entry:
            qs.filter(type_entry=g.type_entry)

        value = qs.aggregate(total_value=Sum("debit"))["total_value"]
        can_use = g.value - value if value else 0

        data.append(f"Goal: {g.name} - Target: {g.value} - Used: {value} - Can Use: {can_use}")

    return data


def get_ini_and_end_date(g: Goal) -> Tuple:

    if g.period == 1:
        week_day = datetime.datetime.now().isocalendar()[1]
        w = Week(datetime.datetime.now().year, week_day)
        start_date = w.monday()
        end_date = w.sunday()

        return start_date, end_date

    raise Exception("Invalid goal.")
