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


def write_json(obj, fn):
    """
    docstring
    """
    with open(fn, 'wt') as outfile:
        outfile.write(json.dumps(obj, indent=2))


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        limit = 1000
        offset = 0
        dataset_code = '8y4t-faws'
        complaints = Complaint.objects.filter(step=0)[:50]
        processed_ids = set()
        ids = ','.join([f"'{c.bbl}'" for c in complaints])
        with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
            taxes = client.get(
                dataset_code, where=f"parid in({ids})")

        for complaint in complaints:
            Property.objects.filter(parid=complaint.bbl).delete()

            for tax in taxes:
                Property.objects.create(
                    parid=complaint.bbl,

                )

            processed_ids.add(complaint.id)

        Complaint.objects.filter(id__in=processed_ids).update(step=1)
