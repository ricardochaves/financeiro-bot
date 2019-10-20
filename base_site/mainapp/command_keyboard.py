from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import TypeEntry
from telepot.namedtuple import InlineKeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup


class CommandKeyBoard:
    def __init__(self, cal):
        self.cal = cal

    def get_entry_date(self):
        return self.cal.get_calendar()

    def get_payment_date(self):
        return self.cal.get_calendar()

    @staticmethod
    def get_category():
        categorys = Category.objects.all()
        k = []
        in_line = []
        count = 0
        for c in categorys:
            count += 1
            k.append(InlineKeyboardButton(text=c.name, callback_data=c.name))
            if count > 2:
                in_line.append(k)
                k = []
                count = 0

        return InlineKeyboardMarkup(inline_keyboard=in_line)

    @staticmethod
    def get_name():
        names = FamilyMember.objects.all()
        k = []
        in_line = []
        count = 0
        for n in names:
            count += 1
            k.append(InlineKeyboardButton(text=n.name, callback_data=n.name))
            if count == 1:
                in_line.append(k)
                k = []
                count = 0

        return InlineKeyboardMarkup(inline_keyboard=in_line)

    @staticmethod
    def get_need_type():
        names = TypeEntry.objects.all()
        k = []
        in_line = []
        count = 0
        for n in names:
            count += 1
            k.append(InlineKeyboardButton(text=n.name, callback_data=n.name))
            if count == 1:
                in_line.append(k)
                k = []
                count = 0

        return InlineKeyboardMarkup(inline_keyboard=in_line)

    @staticmethod
    def get_payment_installments():

        in_line = [
            [
                InlineKeyboardButton(text="1", callback_data="1"),
                InlineKeyboardButton(text="2", callback_data="2"),
                InlineKeyboardButton(text="3", callback_data="3"),
                InlineKeyboardButton(text="4", callback_data="4"),
            ],
            [
                InlineKeyboardButton(text="5", callback_data="5"),
                InlineKeyboardButton(text="6", callback_data="6"),
                InlineKeyboardButton(text="7", callback_data="7"),
                InlineKeyboardButton(text="8", callback_data="8"),
            ],
            [
                InlineKeyboardButton(text="9", callback_data="9"),
                InlineKeyboardButton(text="10", callback_data="10"),
                InlineKeyboardButton(text="11", callback_data="11"),
                InlineKeyboardButton(text="12", callback_data="12"),
            ],
        ]

        return InlineKeyboardMarkup(inline_keyboard=in_line)
