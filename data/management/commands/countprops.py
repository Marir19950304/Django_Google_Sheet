from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from data.models import *
import json

import pytz
import os
load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        complaints = Complaint.objects.all()
        for complaint in complaints:
            print("Prop count:{}".format(
                Property.objects.filter(parid=complaint.bbl).count()))
