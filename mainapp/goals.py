import asyncio
import datetime
import logging

import telepot
from django.conf import settings
from django.db.models import Func
from django.db.models import IntegerField
from django.db.models import Sum
from isoweek import Week

from mainapp.models import Records


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

            bot = telepot.aio.Bot(settings.TELEGRAN_TOKEN)

            loop.run_until_complete(
                bot.sendMessage(
                    self.user_id,
                    f"Você ainda pode gastar {can_use} doas 770 reais estipulados para a semana.",
                )
            )

        except BaseException as e:
            logging.exception("Error na meta", e)
