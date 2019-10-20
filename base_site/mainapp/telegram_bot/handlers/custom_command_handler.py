from typing import Callable
from typing import List

from telegram import MessageEntity
from telegram import Update
from telegram.ext import Handler


class CustomCommandHandle(Handler):
    def __init__(
        self,
        commands_callback: Callable[[], List[str]],
        callback: Callable,
        pass_update_queue=False,
        pass_job_queue=False,
        pass_user_data=False,
        pass_chat_data=False,
    ):
        super(CustomCommandHandle, self).__init__(
            callback,
            pass_update_queue=pass_update_queue,
            pass_job_queue=pass_job_queue,
            pass_user_data=pass_user_data,
            pass_chat_data=pass_chat_data,
        )
        self.commands_callback = commands_callback

    def check_update(self, update):
        """Determines whether an update should be passed to this handlers :attr:`callback`.
        Args:
            update (:class:`telegram.Update`): Incoming telegram update.
        Returns:
            :obj:`list`: The list of args for the handler
        """
        if isinstance(update, Update) and update.effective_message:
            message = update.effective_message

            if (
                message.entities
                and message.entities[0].type == MessageEntity.BOT_COMMAND
                and message.entities[0].offset == 0
            ):
                command = message.text[1 : message.entities[0].length]
                args = message.text.split()[1:]
                command = command.split("@")
                command.append(message.bot.username)

                if not (
                    command[0].lower() in self.list_commands() and command[1].lower() == message.bot.username.lower()
                ):
                    return None

                return args

    def list_commands(self) -> List[str]:
        return self.commands_callback()
