import asyncio
import logging
import os

from django.conf import settings
from pynubank import Nubank
from qrcode.image.pil import PilImage

import telepot.aio
import telepot.aio.helper
from base_site.mainapp.business.command_flow import CommandFlow
from base_site.mainapp.goals import get_goals
from base_site.mainapp.manageconnections import make_sure_mysql_usable
from base_site.mainapp.models import FullCommand
from base_site.mainapp.telegram_bot.calendar import Calendar
from base_site.nubank.models import NubankCards
from base_site.nubank.nubank_bot import NubankBot
from telepot import glance
from telepot import message_identifier
from telepot.aio.delegate import create_open
from telepot.aio.delegate import include_callback_query_chat_id
from telepot.aio.delegate import pave_event_space
from telepot.aio.delegate import per_chat_id
from telepot.aio.loop import MessageLoop

logger = logging.getLogger(__name__)

"""
$ python3.5 lovera.py <token>

1. Send him a message
2. He will ask you to marry him
3. He will keep asking until you say "Yes"

If you are silent for 10 seconds, he will go away a little bit, but is still
there waiting for you. What a sweet bot!

It statically captures callback query according to the originating chat id.
This is the chat-centric approach.

Proposing is a private matter. This bot only works in a private chat.
"""


class Lover(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Lover, self).__init__(*args, **kwargs)

        self.flow = None
        self.cal = Calendar()
        self._edit_msg_ident = None
        self._editor = None
        self.nu = NubankBot()

    async def _cancel_last(self):
        if self._editor:
            await self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None

    async def _send_or_close(self, msg):

        result = self.flow.next(msg)
        if result["done"]:
            await self._close()
            return

        logger.info(f'message: {result["message"]}')
        await self._send_msg(result["message"], keyboard=result["keyboard"])

    async def _close(self):
        await self._send_msg("Enviando seu registro ao Google, aguarde...")
        self.flow.save()
        self.flow = None
        try:
            await self._cancel_last()
        except BaseException:
            logger.info("Não deu.")

        await self._send_msg("Seu registro foi efetuado com sucesso")
        try:
            self.close()
        except BaseException as e:
            logger.info(f"Error: {e}")

    async def _send_msg(self, msg, keyboard=None):
        sent = await self.sender.sendMessage(msg, reply_markup=keyboard)
        self._editor = telepot.aio.helper.Editor(self.bot, sent)
        self._edit_msg_ident = message_identifier(sent)

    async def on_chat_message(self, msg):
        make_sure_mysql_usable()
        logger.info(msg)

        if msg["text"] == "/c":
            commands = FullCommand.objects.order_by("command").all()
            msg = "\n".join([c.command for c in commands])
            await self._send_msg(msg)
            return

        if msg["text"] == "/goals":
            goals = get_goals()
            msg = "\n".join([g for g in goals])
            await self._send_msg(msg)
            return

        n = NubankCards.objects.filter(command_1=msg["text"]).filter()
        if n:
            with open(self.nu.get_qr_code(), "rb") as f:
                await self.sender.sendPhoto(f)
            return

        cm = msg["text"].split(" ")
        if len(cm) == 2:
            n = NubankCards.objects.filter(command_2=cm[0]).first()
            if n:
                await bot.deleteMessage(telepot.message_identifier(msg))
                await self._send_msg("Iniciando o processamento")

                self.nu.set_nubank_command(n)
                self.nu.execute(cm[1], cm)

                return

        if not self.flow:
            self.flow = CommandFlow(msg["text"])
            logger.info("Peguei o comando %s e já guardei" % msg["text"])

        await self._send_or_close(msg["text"])

    async def on_callback_query(self, msg):
        logger.info(msg)
        query_id, from_id, query_data = glance(msg, flavor="callback_query")

        if query_data == "c_X":
            return

        if query_data == "c_after":
            sent = await bot.editMessageText(self._edit_msg_ident, "Mudou", reply_markup=self.cal.get_calendar_after())
            self._edit_msg_ident = message_identifier(sent)
            return

        if query_data == "c_before":
            sent = await bot.editMessageText(self._edit_msg_ident, "Mudou", reply_markup=self.cal.get_calendar_before())
            self._edit_msg_ident = message_identifier(sent)
            return

        await self._send_or_close(query_data)

    async def on__idle(self, event):
        await self.sender.sendMessage("O tempo acabou, o lançamento foi cancelado.")
        self.close()


bot = telepot.aio.DelegatorBot(
    settings.TELEGRAM_TOKEN,
    [
        include_callback_query_chat_id(pave_event_space())(
            per_chat_id(types=["private"]), create_open, Lover, timeout=10
        )
    ],
)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
logger.info("Listening ...")

loop.run_forever()
