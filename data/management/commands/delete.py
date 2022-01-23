from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from data.models import *
from data.tasks import *
import json
from django.db.models import Count, Max
import pytz
import os
load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")


def write_json(obj, fn):
    """
    docstring
    """
    with open(fn, 'wt') as outfile:
        outfile.write(json.dumps(obj, indent=2))


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument("--what")

    def handle(self, *args, **options):
        delete_all()

