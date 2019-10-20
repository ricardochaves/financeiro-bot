from base_site.mainapp.business.register import Register
from base_site.mainapp.command_keyboard import CommandKeyBoard
from base_site.mainapp.models import FullCommand
from base_site.mainapp.telegram_bot.calendar import Calendar


class NewCommand:
    def __init__(self, txt_command):
        self.register = Register(FullCommand.objects.filter(command=txt_command).first())
        self.start = False
        self.cal = Calendar()
        self.command_keyboard = CommandKeyBoard(self.cal)
