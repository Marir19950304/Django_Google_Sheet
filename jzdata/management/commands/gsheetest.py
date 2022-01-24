
from django.core.management.base import BaseCommand, CommandError

from dotenv import load_dotenv

from jzdata.tasks import *
load_dotenv()


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--type', default = 'fetchfromdate', type = str)
        parser.add_argument('--back-days', default = -1, type = int)

    def handle(self, *args, **options):
        run_task(fetch_type=options['type'], back_days=options['back_days'])
        