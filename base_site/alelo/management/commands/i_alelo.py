from base_site.alelo.tasks import execute_alelo_api
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute_alelo_api()
