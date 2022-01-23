from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from data.models import *
from data.tasks import *
import json

import pytz
import os
load_dotenv()


EST = pytz.timezone("US/Eastern")


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument("--back-days", default=1, type=int)

    def handle(self, *args, **options):
        print(fetch_daily(options['back_days']))
