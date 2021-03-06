from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from jzdata.models import *
from jzdata.tasks import *
import json

import pytz
import os
load_dotenv()


EST = pytz.timezone("US/Eastern")


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        fetch_result()