from typing import List

from base_site.mainapp.models import FullCommand


def get_valid_commands() -> List[str]:
    commands = FullCommand.objects.all()
    return [x.command.replace("/", "") for x in commands]
