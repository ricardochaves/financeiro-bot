from base_site.mainapp.models import FullCommand
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Seed database"

    def handle(self, *args, **options):
        FullCommand.objects.create(command="/a", entry_date=False, payment_date=3)
        FullCommand.objects.create(command="/ac", entry_date=False, payment_date=2)
