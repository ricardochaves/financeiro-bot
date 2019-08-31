import calendar
from datetime import datetime

from dateutil.relativedelta import relativedelta
from telepot.namedtuple import InlineKeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup


class Calendar:
    def __init__(self):

        self.c = calendar.TextCalendar(calendar.SUNDAY)
        self.date_now = datetime.now()

    def get_calendar(self):

        k_calendar = [
            [
                InlineKeyboardButton(text="<", callback_data="c_before"),
                InlineKeyboardButton(text=f"{self._get_header()}", callback_data="c_X"),
                InlineKeyboardButton(text=">", callback_data="c_after"),
            ],
            [
                InlineKeyboardButton(text="D", callback_data="c_X"),
                InlineKeyboardButton(text="S", callback_data="c_X"),
                InlineKeyboardButton(text="T", callback_data="c_X"),
                InlineKeyboardButton(text="Q", callback_data="c_X"),
                InlineKeyboardButton(text="Q", callback_data="c_X"),
                InlineKeyboardButton(text="S", callback_data="c_X"),
                InlineKeyboardButton(text="S", callback_data="c_X"),
            ],
        ]

        days = list(self._get_days_from_month_year())

        days = [InlineKeyboardButton(text=self.get_day_text(d), callback_data=self.get_day_value(d)) for d in days]

        k_calendar += [days[x : x + 7] for x in range(0, len(days), 7)]

        return InlineKeyboardMarkup(inline_keyboard=k_calendar)

    def _get_header(self):
        return f"{calendar.month_name[self.date_now.month]} {self.date_now.year}"

    def _get_days_from_month_year(self):

        return self.c.itermonthdays(self.date_now.year, self.date_now.month)

    def get_calendar_before(self):
        self.date_now = self.date_now + relativedelta(months=-1)
        return self.get_calendar()

    def get_calendar_after(self):
        self.date_now = self.date_now + relativedelta(months=+1)
        return self.get_calendar()

    @staticmethod
    def get_day_text(day):
        return " " if day == 0 else day

    def get_day_value(self, day):
        if day == 0:
            return "c_X"

        return f"c_d_{day}-{self.date_now.month}-{self.date_now.year}"

    @staticmethod
    def convert_calendar_day_value_to_datetime(value):
        return datetime.strptime(value.replace("c_d_", ""), "%d-%m-%Y")
