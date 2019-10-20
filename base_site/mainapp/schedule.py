import asyncio
import json
import logging
from datetime import date
from datetime import datetime
from datetime import time

import arrow
import telepot
from base_site.mainapp.models import Records
from django.conf import settings
from telepot.aio.loop import MessageLoop


def execute_command(str_dict):
    # Create dict
    data = json.loads(str_dict)

    # Check days key
    if "days" in data.keys():
        now = datetime.now()
        if now.strftime("%A") not in data["days"]:
            logging.warning("Not execute today!")
            return

    if "verify" in data.keys():

        filters = data["verify"]["query"]

        if data["verify"]["when"] == "day":
            today_min = datetime.combine(date.today(), time.min)
            today_max = datetime.combine(date.today(), time.max)
            filters["create_date_time__range"] = (today_min, today_max)

        elif data["verify"]["when"] == "month":
            last_day = arrow.utcnow().ceil("month").date()

            start = datetime.combine(date.today().replace(day=1), time.min)
            end = datetime.combine(last_day, time.max)
            filters["create_date_time__range"] = (start, end)

        r = Records.objects.filter(**filters).all()
        if r:
            logging.warning("Achei")
            return

    loop = asyncio.get_event_loop()

    bot = telepot.aio.Bot(settings.TELEGRAM_TOKEN)

    loop.run_until_complete(bot.sendMessage(data["message"]["user"], data["message"]["text"]))
